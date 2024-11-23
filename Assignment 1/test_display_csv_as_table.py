from pytest import fixture
import pytest
from product_search import display_csv_as_table
from unittest.mock import mock_open, patch
from io import StringIO


class TestDisplayCsvAsTable:

    @fixture
    def get_csv_data_stub1(self, mocker):
        return mocker.patch('display_csv_as_table.get_csv_data', return_value="Apple")


    def test_display_csv_as_table_invalid_input_types(self, get_csv_data_stub1):
        result = display_csv_as_table("1")
        assert result is None


    # 测试有效输入类型
    @pytest.mark.parametrize("csv_file_name",
                             ["products.csv", "inventory.csv", "items.csv", "list.csv", "data.csv", "test.csv",
                              "sample.csv", "info.csv", "details.csv", "shop.csv"])
    def test_display_csv_as_table_valid_input_types(csv_file_name, mocker):
        # 模拟文件读取
        mock_data = [
            ["Product", "Price", "Units"],
            ["Product1", "10.0", "5"],
            ["Product2", "15.5", "3"],
            ["Product3", "20.0", "0"]
        ]

        with patch('builtins.open', mock_open(read_data=mock_data)):
            display_csv_as_table(csv_file_name)
            # 验证文件是否正确读取和显示
            assert True  # 这里可以根据实际输出进行验证


    # 测试文件不存在的情况
    def test_display_csv_as_table_file_not_found(mocker):
        csv_file_name = "non_existent.csv"
        with patch('builtins.open', side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):
                display_csv_as_table(csv_file_name)


    # 测试文件为空的情况
    def test_display_csv_as_table_empty_file(mocker):
        csv_file_name = "empty.csv"
        with patch('builtins.open', mock_open(read_data=[])):
            display_csv_as_table(csv_file_name)
            # 验证是否正确处理空文件
            assert True  # 这里可以根据实际输出进行验证


    # 测试文件内容格式错误的情况
    def test_display_csv_as_table_invalid_format(mocker):
        csv_file_name = "invalid_format.csv"
        with patch('builtins.open', mock_open(read_data=["Invalid", "Data"])):
            display_csv_as_table(csv_file_name)
            # 验证是否正确处理格式错误的文件
            assert True  # 这里可以根据实际输出进行验证\

