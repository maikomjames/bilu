import pytest
from pydantic import ValidationError

from bilu.model import BaseModel

pytestmark = pytest.mark.asyncio


class TestBaseModel:

    @pytest.fixture
    def value_attrs(self):
        return {
            'attr_str': 'bla',
            'attr_int': 123
        }

    @pytest.fixture
    def model(self):

        class TesteModel(BaseModel):
            attr_str: str
            attr_int: int

            class Meta:
                name = 'testemodel'

        return TesteModel

    @pytest.fixture
    async def model_saved(self, setup_db, model, value_attrs):
        model_test = model(
            **value_attrs
        )
        return await model_test.save()

    async def test_list_success(
        self,
        setup_db,
        model,
        model_saved,
        value_attrs
    ):
        result = await model.documents.list(
            _id=model_saved.inserted_id
        )
        assert len(result) == 1
        assert result[0].attr_str == value_attrs.get('attr_str')
        assert result[0].attr_int == value_attrs.get('attr_int')

    async def test_save_success(self, setup_db, model, value_attrs):
        model_test = model(
            attr_str='oioioi',
            attr_int=2
        )
        model_saved = await model_test.save()

        assert model_saved.inserted_id

    async def test_should_fail_to_save_with_invalid_data(
        self,
        setup_db,
        model
    ):
        with pytest.raises(ValidationError):
            model(
                attr_str=123,
                attr_int='oioio'
            )

    async def test_get_success(
        self,
        setup_db,
        model,
        model_saved,
        value_attrs
    ):
        result = await model.documents.get(
            attr_str=value_attrs.get('attr_str')
        )
        assert result

    async def test_get_not_found(
        self,
        setup_db,
        model,
        model_saved
    ):
        result = await model.documents.get(
            attr_str='banana'
        )
        assert result is None

    async def test_delete_success(
        self,
        setup_db,
        model,
        model_saved,
        value_attrs
    ):
        result = await model.documents.get(
            attr_str=value_attrs.get('attr_str')
        )
        await result.delete()

        result_not_found = await model.documents.get(
            attr_str=value_attrs.get('attr_str')
        )
        assert result_not_found is None

    async def test_should_update_success(
        self,
        setup_db,
        model,
        model_saved,
        value_attrs
    ):
        result = await model.documents.get(
            attr_str=value_attrs.get('attr_str')
        )

        assert result.attr_str == value_attrs.get('attr_str')
        assert result.attr_int == value_attrs.get('attr_int')

        result.attr_str = 'updated'
        result.attr_int = 99999

        await result.save()

        result_updated = await model.documents.get(
            _id=result._id
        )

        assert result_updated.attr_str == 'updated'
        assert result_updated.attr_int == 99999

    async def test_should_fail_to_update_with_invalid_data(
        self,
        setup_db,
        model,
        model_saved,
        value_attrs
    ):
        result = await model.documents.get(
            attr_str=value_attrs.get('attr_str')
        )

        assert result.attr_str == value_attrs.get('attr_str')
        assert result.attr_int == value_attrs.get('attr_int')

        result.attr_str = 'updated'
        result.attr_int = {}

        with pytest.raises(ValidationError):
            await result.save()

    async def test_should_not_save_extra_attrs(
        self,
        setup_db,
        model,
        value_attrs
    ):
        model_test = model(
            extra_attr='ignored',
            **value_attrs
        )
        await model_test.save()

        result = await model.documents.get(
            _id=model_test._id
        )

        assert result
        assert getattr(result, 'extra_attr', None) is None
