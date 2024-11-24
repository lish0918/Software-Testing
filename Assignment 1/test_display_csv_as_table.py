from pytest import fixture, raises
from online_shopping_cart.product.product_search import display_csv_as_table
import shutil
import os


class TestDisplayCsvAsTable:

    @fixture
    def copy_csv_file(self, tmp_path):
        original_file_path = "files/products.csv"
        temp_file_path = tmp_path / "products.csv"
        shutil.copyfile(original_file_path, temp_file_path) # copy the original CSV file to the temporary path
        yield temp_file_path # provide the temporary file path to the test
        os.remove(temp_file_path) # delete the temporary file after the test


    # Invalid input type - int
    def test_int_input(copy_csv_file):
        with raises(OSError) as excinfo:
            display_csv_as_table(123)
        assert "[WinError 6] 句柄无效。" in str(excinfo.value)

    # Invalid input type - float
    def test_float_input(copy_csv_file):
        with raises(TypeError) as excinfo:
            display_csv_as_table(1.0)
        assert "expected str, bytes or os.PathLike object, not float" in str(excinfo.value)

    # Invalid input type - list
    def test_list_input(copy_csv_file):
        with raises(TypeError) as excinfo:
            display_csv_as_table([1,2,3])
        assert "expected str, bytes or os.PathLike object, not list" in str(excinfo.value)

    # Filename input - empty string
    def test_empty_string_input(copy_csv_file):
        with raises(FileNotFoundError) as excinfo:
            display_csv_as_table("")
        assert "No such file or directory" in str(excinfo.value)

    # Input right filename
    def test_right_filename(self, copy_csv_file, capsys):
        copy_csv_file = copy_csv_file.parent / "products_copy.csv"
        shutil.copyfile("files/products.csv", copy_csv_file)
        display_csv_as_table(copy_csv_file)
        out, err = capsys.readouterr()
        assert "['Product', 'Price', 'Units']" in out
        assert "['Apple', '2', '10']" in out

    # Input right filename with spaces
    def test_valid_filename_with_spaces(self, copy_csv_file, capsys):
        copy_csv_file = copy_csv_file.parent / "products copy.csv"
        shutil.copyfile("files/products.csv", copy_csv_file)
        display_csv_as_table(copy_csv_file)
        out, err = capsys.readouterr()
        assert "['Product', 'Price', 'Units']" in out
        assert "['Apple', '2', '10']" in out

    # Input right filename with special characters
    def test_valid_filename_with_special_characters(self, copy_csv_file, capsys):
        copy_csv_file = copy_csv_file.parent / "products@copy.csv"
        shutil.copyfile("files/products.csv", copy_csv_file)
        display_csv_as_table(copy_csv_file)
        out, err = capsys.readouterr()
        assert "['Product', 'Price', 'Units']" in out
        assert "['Apple', '2', '10']" in out

    # Input right filename with different case
    def test_valid_filename_with_different_case(self, copy_csv_file, capsys):
        copy_csv_file = copy_csv_file.parent / "PROdUCTS.csv"
        shutil.copyfile("files/products.csv", copy_csv_file)
        display_csv_as_table(copy_csv_file)
        out, err = capsys.readouterr()
        assert "['Product', 'Price', 'Units']" in out
        assert "['Apple', '2', '10']" in out

    # Input right filename with upper case of extension
    def test_valid_filename_with_different_extensions(self, copy_csv_file, capsys):
        copy_csv_file = copy_csv_file.parent / "products.CSV"
        shutil.copyfile("files/products.csv", copy_csv_file)
        display_csv_as_table(copy_csv_file)
        out, err = capsys.readouterr()
        assert "['Product', 'Price', 'Units']" in out
        assert "['Apple', '2', '10']" in out

    # Display non-csv file
    def test_non_csv_file(self, tmp_path, capsys):
        copy_csv_file = tmp_path / "non_csv.txt"
        copy_csv_file.write_text("Non-CSV content")
        display_csv_as_table(copy_csv_file)
        out, err = capsys.readouterr()
        assert out == "\n['Non-CSV content']\n"

    # Display different foramts of CSV file
    def test_invalid_csv_format(self, tmp_path, capsys):
        copy_csv_file = tmp_path / "invalid.csv"
        copy_csv_file.write_text("Invalid,Data,Format\n1,2,3,4")  # 故意多一个列
        display_csv_as_table(copy_csv_file)
        out, err = capsys.readouterr()
        assert out == "\n['Invalid', 'Data', 'Format']\n['1', '2', '3', '4']\n"

    # Display file with only header
    def test_csv_file_with_only_header(self, tmp_path, capsys):
        copy_csv_file = tmp_path / "header.csv"
        copy_csv_file.write_text("Product,Price,Units")
        display_csv_as_table(copy_csv_file)
        out, err = capsys.readouterr()
        assert out == "\n['Product', 'Price', 'Units']\n"

    # Display file with only one row
    def test_csv_file_with_one_row(self, tmp_path, capsys):
        copy_csv_file = tmp_path / "one_row.csv"
        copy_csv_file.write_text("Apple,2,10")
        display_csv_as_table(copy_csv_file)
        out, err = capsys.readouterr()
        assert out == "\n['Apple', '2', '10']\n"

    # Display file with multiple rows
    def test_csv_file_with_multiple_rows(self, tmp_path, capsys):
        copy_csv_file = tmp_path / "multiple_rows.csv"
        copy_csv_file.write_text("Product,Price,Units\nApple,2,10\nBanana,1,5")
        display_csv_as_table(copy_csv_file)
        out, err = capsys.readouterr()
        assert out == "\n['Product', 'Price', 'Units']\n['Apple', '2', '10']\n['Banana', '1', '5']\n"
    


    

