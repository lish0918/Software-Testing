from pytest import fixture, raises
from online_shopping_cart.product.product_search import display_filtered_table
import shutil
import os


class TestDisplayFilteredTable:

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
            display_filtered_table(123, "apple")
        assert "[WinError 6] 句柄无效。" in str(excinfo.value)

    # Invalid input type - float
    def test_float_input(copy_csv_file):
        with raises(TypeError) as excinfo:
            display_filtered_table(1.0, "apple")
        assert "expected str, bytes or os.PathLike object, not float" in str(excinfo.value)

    # Invalid input type - list
    def test_list_input(copy_csv_file):
        with raises(TypeError) as excinfo:
            display_filtered_table([1,2,3], "apple")
        assert "expected str, bytes or os.PathLike object, not list" in str(excinfo.value)
    
     # Search target - int
    def test_search_target_int(self, copy_csv_file):
        with raises(AttributeError) as excinfo:
            display_filtered_table(copy_csv_file, 123)
        assert "'int' object has no attribute 'capitalize'" in str(excinfo.value)

    # Search target - float
    def test_search_target_float(self, copy_csv_file):
        with raises(AttributeError) as excinfo:
            display_filtered_table(copy_csv_file, 1.0)
        assert "'float' object has no attribute 'capitalize'" in str(excinfo.value)

    # Search target - list 
    def test_search_target_list(self, copy_csv_file):
        with raises(AttributeError) as excinfo:
            display_filtered_table(copy_csv_file, [1,2,3])
        assert "'list' object has no attribute 'capitalize'" in str(excinfo.value)

    # Search target - empty string
    def test_empty_search_target(self, copy_csv_file, capsys):
        display_filtered_table(copy_csv_file, "")
        out, err = capsys.readouterr()
        assert out == "\n['Product', 'Price', 'Units']\n"

    # Filename input - empty string
    def test_empty_string_input(copy_csv_file):
        with raises(FileNotFoundError) as excinfo:
            display_filtered_table("", "apple")
        assert "No such file or directory" in str(excinfo.value)

    # Input right filename
    def test_right_filename(self, copy_csv_file, capsys):
        copy_csv_file = copy_csv_file.parent / "products_copy.csv"
        shutil.copyfile("files/products.csv", copy_csv_file)
        display_filtered_table(copy_csv_file, "apple")
        out, err = capsys.readouterr()
        assert "['Product', 'Price', 'Units']" in out
        assert "['Apple', '2', '10']" in out

    # Input right filename with spaces
    def test_valid_filename_with_spaces(self, copy_csv_file, capsys):
        copy_csv_file = copy_csv_file.parent / "products copy.csv"
        shutil.copyfile("files/products.csv", copy_csv_file)
        display_filtered_table(copy_csv_file, "apple")
        out, err = capsys.readouterr()
        assert "['Product', 'Price', 'Units']" in out
        assert "['Apple', '2', '10']" in out

    # Input right filename with special characters
    def test_valid_filename_with_special_characters(self, copy_csv_file, capsys):
        copy_csv_file = copy_csv_file.parent / "prod%ucts@copy.csv"
        shutil.copyfile("files/products.csv", copy_csv_file)
        display_filtered_table(copy_csv_file, "apple")
        out, err = capsys.readouterr()
        assert "['Product', 'Price', 'Units']" in out
        assert "['Apple', '2', '10']" in out

    # Input right filename with different case
    def test_valid_filename_with_different_case(self, copy_csv_file, capsys):
        copy_csv_file = copy_csv_file.parent / "PROdUCTS.csv"
        shutil.copyfile("files/products.csv", copy_csv_file)
        display_filtered_table(copy_csv_file, "apple")
        out, err = capsys.readouterr()
        assert "['Product', 'Price', 'Units']" in out
        assert "['Apple', '2', '10']" in out

    # Input right filename with diffrent case of extension
    def test_valid_filename_with_different_extensions(self, copy_csv_file, capsys):
        copy_csv_file = copy_csv_file.parent / "products_copy.cSv"
        shutil.copyfile("files/products.csv", copy_csv_file)
        display_filtered_table(copy_csv_file, "apple")
        out, err = capsys.readouterr()
        assert "['Product', 'Price', 'Units']" in out
        assert "['Apple', '2', '10']" in out

    # Search target - upper case
    def test_search_target_upper_case(self, copy_csv_file, capsys):
        display_filtered_table(copy_csv_file, "APPLE")
        out, err = capsys.readouterr()
        assert out == "\n['Product', 'Price', 'Units']\n['Apple', '2', '10']\n"

    # Search target - different case
    def test_search_target_different_case(self, copy_csv_file, capsys):
        display_filtered_table(copy_csv_file, "aPpLe")
        out, err = capsys.readouterr()
        assert out == "\n['Product', 'Price', 'Units']\n['Apple', '2', '10']\n"

    # Search target - special characters
    def test_search_target_special_characters(self, copy_csv_file, capsys):
        display_filtered_table(copy_csv_file, "aPp@e")
        out, err = capsys.readouterr()
        assert out == "\n['Product', 'Price', 'Units']\n"

    # Search target - non-existing product
    def test_search_target_non_existing_product(self, copy_csv_file, capsys):
        display_filtered_table(copy_csv_file, "house")
        out, err = capsys.readouterr()
        assert out == "\n['Product', 'Price', 'Units']\n"

    # Search target - multiple products
    def test_search_target_multiple_products(self, copy_csv_file, capsys):
        display_filtered_table(copy_csv_file, "apple, banana")
        out, err = capsys.readouterr()
        assert out == "\n['Product', 'Price', 'Units']\n['Apple', '2', '10']\n['Banana', '1', '15']\n"

    # Search target - multiple products with special characters
    def test_search_target_multiple_products_with_spaces(self, copy_csv_file, capsys):
        display_filtered_table(copy_csv_file, "apple&banana")
        out, err = capsys.readouterr()
        assert out == "\n['Product', 'Price', 'Units']\n['Apple', '2', '10']\n['Banana', '1', '15']\n"


   

