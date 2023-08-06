import pytest
from pydantic import Field
from ..mort_jams import (
    UIProp,
    FormModel,
    FormProp,
    UIHidden,
    FormSchema,
    UISchemaConfig,
)


def test_json_and_ui_schema_serialize():
    class TestForm(FormModel):
        attribute: str = FormProp(..., ui=UIHidden)

    output = FormSchema(**TestForm.form_schema())
    assert output is not None
    # required field in JSONSchema
    assert "attribute" in output.data["required"]
    # hidden widget UI attribute
    assert output.data["properties"]["attribute"].get("ui", None) is None
    assert output.ui.properties["attribute"].widget == "hidden"


def test_model_ui_schema_works_with_non_ui_fields():
    class TestForm(FormModel):

        attribute: str = Field(..., description="plain field")

    output = FormSchema(**TestForm.form_schema())
    assert output is not None


def test_form_model_config_can_include_schema_config():
    class TestForm(FormModel):
        class Config:
            ui = UISchemaConfig(title="sweet")

        attribute: str = Field(..., description="plain field")

    output = FormSchema(**TestForm.form_schema())
    assert output is not None
