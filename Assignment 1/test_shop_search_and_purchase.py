from pytest import fixture, raises
from online_shopping_cart.shop.shop_search_and_purchase import search_and_purchase_product


class TestSearchAndPurchaseProduct:
    @fixture
    def login_stub(self, mocker):
        return mocker.patch('online_shopping_cart.shop.shop_search_and_purchase.login',
                            return_value={'username': 'Alex', 'wallet': '100.0'})

    @fixture
    def user_input_stub(self, mocker):
        return mocker.patch('online_shopping_cart.user.user_interface.UserInterface.get_user_input')

    @fixture
    def display_csv_stub(self, mocker):
        return mocker.patch('online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table',
                            return_value=[["Product", "Price", "Units"],
                                          ["Apple", 2, 10],
                                          ["Banana", 1, 15]])

    @fixture
    def display_filtered_stub(self, mocker):
        return mocker.patch('online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table',
                            return_value=[["Product", "Price", "Units"],
                                          ["Apple", 2, 10]])

    @fixture
    def checkout_stub(self, mocker):
        return mocker.patch('online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment',
                            return_value={'username': 'Alex', 'password': '1234'})

    # Search for a product using the int
    def test_search_product_using_int(self, login_stub, user_input_stub):
        user_input_stub.side_effect = [1, 'y']
        with raises(AttributeError) as excinfo:
            search_and_purchase_product()

        assert "'int' object has no attribute 'lower'" in str(excinfo.value)

    # Search for a product using the float
    def test_search_product_using_float(self, login_stub, user_input_stub):
        user_input_stub.side_effect = [1.5, 'y']
        with raises(AttributeError) as excinfo:
            search_and_purchase_product()

        assert "'float' object has no attribute 'lower'" in str(excinfo.value)

    # Search for a product using the list
    def test_search_product_using_list(self, login_stub, user_input_stub):
        user_input_stub.side_effect = [[1, 2, 3], 'y']
        with raises(AttributeError) as excinfo:
            search_and_purchase_product()

        assert "'list' object has no attribute 'lower'" in str(excinfo.value)


    # Search for a product using wrong string
    def test_search_product_using_wrong_string(self, login_stub, user_input_stub, display_filtered_stub, checkout_stub):
        user_input_stub.side_effect = ['HOUSE', 'y']
        search_and_purchase_product()
        login_stub.assert_called_once()
        display_filtered_stub.assert_called_once()
        checkout_stub.assert_called_once()

    # Display one filtered product
    def test_display_filtered_products_1(self, login_stub, user_input_stub, display_filtered_stub, checkout_stub):
        user_input_stub.side_effect = ['Apple', 'y']
        search_and_purchase_product()
        login_stub.assert_called_once()
        display_filtered_stub.assert_called_once_with(search_target="apple")
        checkout_stub.assert_called_once()

    # Display one filtered product with wrong case
    def test_display_filtered_products_2(self, login_stub, user_input_stub, display_filtered_stub, checkout_stub):
        user_input_stub.side_effect = ['apPle', 'Y']
        search_and_purchase_product()
        login_stub.assert_called_once()
        display_filtered_stub.assert_called_once_with(search_target="apple")
        checkout_stub.assert_called_once()

    # Display two filtered products
    def test_display_filtered_products_3(self, login_stub, user_input_stub, display_filtered_stub, checkout_stub):
        user_input_stub.side_effect = ['Apple', 'n', 'Banana', 'y']
        search_and_purchase_product()
        login_stub.assert_called_once()
        display_filtered_stub.assert_called_with(search_target="banana")
        assert display_filtered_stub.call_count == 2
        checkout_stub.assert_called_once()

    # Display all products
    def test_display_all_products_1(self, login_stub, user_input_stub, display_csv_stub, checkout_stub):
        user_input_stub.side_effect = ['all', 'y']
        search_and_purchase_product()
        login_stub.assert_called_once()
        display_csv_stub.assert_called_once()
        checkout_stub.assert_called_once()

    # Display all products in wrong case
    def test_display_all_products_2(self, login_stub, user_input_stub, display_csv_stub, checkout_stub):
        user_input_stub.side_effect = ['AlL', 'Y']
        search_and_purchase_product()
        login_stub.assert_called_once()
        display_csv_stub.assert_called_once()
        checkout_stub.assert_called_once()

    # Display all products first twice
    def test_display_all_products_3(self, login_stub, user_input_stub, display_csv_stub, checkout_stub):
        user_input_stub.side_effect = ['all', 'n', 'all', 'y']
        search_and_purchase_product()
        login_stub.assert_called_once()
        assert display_csv_stub.call_count == 2
        checkout_stub.assert_called_once()

    # Display all products first and then display one filtered product
    def test_display_all_products_and_filtered_products_1(self, login_stub, user_input_stub, display_csv_stub, display_filtered_stub, checkout_stub):
        user_input_stub.side_effect = ['all', 'n', 'Apple', 'y']
        search_and_purchase_product()
        login_stub.assert_called_once()
        display_csv_stub.assert_called_once()
        display_filtered_stub.assert_called_once_with(search_target="apple")
        checkout_stub.assert_called_once()

    # Display all products first and then display two filtered products
    def test_display_all_products_and_filtered_products_2(self, login_stub, user_input_stub, display_csv_stub, display_filtered_stub, checkout_stub):
        user_input_stub.side_effect = ['all', 'n', 'Apple', 'n', 'Banana', 'y']
        search_and_purchase_product()
        login_stub.assert_called_once()
        display_csv_stub.assert_called_once()
        display_filtered_stub.assert_called_with(search_target="banana")
        assert display_filtered_stub.call_count == 2
        checkout_stub.assert_called_once()

    # Display one filtered product first and then display all products
    def test_display_all_products_and_filtered_products_3(self, login_stub, user_input_stub, display_csv_stub, display_filtered_stub, checkout_stub):
        user_input_stub.side_effect = ['LAPTOP', 'n', 'all', 'y']
        search_and_purchase_product()
        login_stub.assert_called_once()
        display_filtered_stub.assert_called_once_with(search_target="laptop")
        display_csv_stub.assert_called_once()
        checkout_stub.assert_called_once()

    # Display two filtered products first and then display all products
    def test_display_all_products_and_filtered_products_4(self, login_stub, user_input_stub, display_csv_stub, display_filtered_stub, checkout_stub):
        user_input_stub.side_effect = ['Apple', 'n', 'Grapes', 'n', 'all', 'y']
        search_and_purchase_product()
        login_stub.assert_called_once()
        display_filtered_stub.assert_called_with(search_target="grapes")
        assert display_filtered_stub.call_count == 2
        display_csv_stub.assert_called_once()
        checkout_stub.assert_called_once()

    # Display products multiple times in diffrent ways
    def test_display_all_products_and_filtered_products_5(self, login_stub, user_input_stub, display_csv_stub, display_filtered_stub, checkout_stub):
        user_input_stub.side_effect = ['all', 'n', 'Apple', 'n', 'Banana', 'n', 'all', 'y']
        search_and_purchase_product()
        login_stub.assert_called_once()
        assert display_csv_stub.call_count == 2
        assert display_filtered_stub.call_count == 2
        checkout_stub.assert_called_once()
    
    
