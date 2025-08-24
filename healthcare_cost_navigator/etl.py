#!/usr/bin/env python
"""
Entry point for the ETL process.
"""

import os
import csv
from io import StringIO
import sys

import click
from sqlmodel import create_engine, Session, select

from healthcare_cost_navigator.models.etl import ProviderAndService
from healthcare_cost_navigator.models.service import State, Provider, Service


def try_open_file(file_path: str):
    """Try to open file with different encodings"""
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "iso-8859-1"]

    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                content = f.read()
                return content, encoding
        except UnicodeDecodeError as e:
            print(f"Failed with {encoding}: {e}")
            continue

    raise ValueError(f"Could not decode file with any of the encodings: {encodings}")


# pylint: disable=too-many-locals
@click.command(name="etl")
@click.option(
    "--file",
    type=click.Path(exists=True),
    required=True,
)
@click.option(
    "--database-url",
    type=str,
    default=os.getenv(
        "DATABASE_URL", "postgresql+psycopg://hcn:hcn@localhost:54321/hcn"
    ),
)
def main(file: str, database_url: str) -> None:
    """
    Entry point for the ETL process.
    """
    engine = create_engine(database_url)
    with Session(engine) as session:
        try:
            content, encoding = try_open_file(file)
            print(f"Successfully opened file with encoding: {encoding}")

            file_handle = StringIO(content)

            reader = csv.DictReader(file_handle)
            rows_processed = 0
            for row in reader:
                try:
                    if rows_processed % 1000 == 0:
                        print(f"Processing row #{rows_processed + 1}")
                    row_lowercased_keys = {k.lower(): v for k, v in row.items() if v}
                    provider_and_service = ProviderAndService(**row_lowercased_keys)  # type: ignore

                    # Find or create the State
                    state = session.exec(
                        select(State).where(
                            State.abbreviation
                            == provider_and_service.rndrng_prvdr_state_abrvtn
                        )
                    ).first()
                    if not state:
                        print(
                            f"Creating new state: {provider_and_service.rndrng_prvdr_state_abrvtn}"
                        )
                        # Create a new state (you might want to add more state data)
                        state = State(
                            abbreviation=provider_and_service.rndrng_prvdr_state_abrvtn,
                            name=provider_and_service.rndrng_prvdr_state_abrvtn,
                            fips_code=0,  # You might want to add proper FIPS codes
                        )
                        session.add(state)
                        session.commit()
                        session.flush()  # Get the ID

                    # Find or create the Provider
                    provider = session.exec(
                        select(Provider).where(
                            Provider.ccn == provider_and_service.rndrng_prvdr_ccn
                        )
                    ).first()
                    if not provider:
                        provider = Provider(
                            ccn=provider_and_service.rndrng_prvdr_ccn,
                            name=provider_and_service.rndrng_prvdr_org_name,
                            city=provider_and_service.rndrng_prvdr_city,
                            state_id=state.id,
                            zip_code_five=provider_and_service.rndrng_prvdr_zip5,
                            rural_commuting_area=0,  # Default value
                            rural_commuting_area_description="Unknown",  # Default value
                        )
                        session.add(provider)
                        session.flush()  # Get the ID

                    service = Service(
                        code=provider_and_service.drg_cd,
                        discharges=provider_and_service.tot_dschrgs,
                        average_covered_charges=provider_and_service.avg_submtd_cvrd_chrg,
                        average_total_payments=provider_and_service.avg_tot_pymt_amt,
                        average_medicare_payments=provider_and_service.avg_mdcr_pymt_amt,
                        provider_id=provider.id,
                    )

                    session.add(service)

                    # print(provider_and_service)
                    rows_processed += 1
                # pylint: disable=broad-exception-caught
                except Exception as e:
                    print(row)
                    print(e)
                    sys.exit(1)
        # pylint: disable=broad-exception-caught
        except Exception as e:
            print(f"Error opening file: {e}")
            sys.exit(1)

    print(f"Processed {rows_processed} rows")


def init() -> None:
    """
    Entry point for the ETL process.
    """

    if __name__ == "__main__":
        # pylint: disable=no-value-for-parameter
        main()


if __name__ == "__main__":
    init()
