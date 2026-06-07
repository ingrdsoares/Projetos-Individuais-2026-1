from pydantic import BaseModel, Field
from typing import List, Optional

class Metric(BaseModel):
    """Represents a single financial or operational metric."""
    name: str = Field(..., description="The name of the metric (e.g., 'Vendas Líquidas', 'Estoque de Unidades')")
    value: Optional[float] = Field(None, description="The numeric value of the metric. Use null if not found.")
    unit: Optional[str] = Field(None, description="The unit of the value (e.g., 'R$', 'milhares', 'unidades')")

class CompanyReport(BaseModel):
    """Structured output for a company's operational report."""
    company_name: str = Field(..., description="Official name of the company")
    year: int = Field(..., description="The reference year of the report")
    quarter: str = Field(..., description="The reference quarter (e.g., '1T', '2T', '3T', '4T')")
    metrics: List[Metric] = Field(..., description="List of extracted metrics")

# This schema will be used by the LLM to ensure structured output.
