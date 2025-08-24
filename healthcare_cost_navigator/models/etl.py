"""
Models for the ETL process.
"""

from pydantic import BaseModel


class ProviderAndService(BaseModel):
    """
    A provider and service.
    """

    rndrng_prvdr_ccn: int
    rndrng_prvdr_org_name: str
    rndrng_prvdr_city: str
    rndrng_prvdr_st: str
    rndrng_prvdr_state_fips: int
    rndrng_prvdr_zip5: str
    rndrng_prvdr_state_abrvtn: str
    rndrng_prvdr_ruca: float | None = None
    rndrng_prvdr_ruca_desc: str | None = None
    drg_cd: str
    drg_desc: str
    tot_dschrgs: int
    avg_submtd_cvrd_chrg: float
    avg_tot_pymt_amt: float
    avg_mdcr_pymt_amt: float
