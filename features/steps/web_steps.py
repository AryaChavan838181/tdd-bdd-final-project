"""Task 7: Browser steps for the product catalogue UI."""
from behave import then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select, WebDriverWait


def field_id(field_name):
    return "product_" + field_name.lower().replace(" ", "_")


@when('I visit the "Home Page"')
def visit_home(context):
    context.driver.get(context.base_url)


@then('I should see "{text}" in the title')
def title_contains(context, text):
    assert text in context.driver.title


@when('I set the "{field}" to "{value}"')
@when('I change "{field}" to "{value}"')
def set_field(context, field, value):
    element = context.driver.find_element(By.ID, field_id(field))
    element.clear()
    element.send_keys(value)


@when('I select "{option}" in the "{field}" dropdown')
def select_dropdown(context, option, field):
    Select(context.driver.find_element(By.ID, field_id(field))).select_by_visible_text(option)


@then('I should see "{option}" in the "{field}" dropdown')
def verify_dropdown(context, option, field):
    select = Select(context.driver.find_element(By.ID, field_id(field)))
    assert select.first_selected_option.text == option


@then('I should see "{value}" in the "{field}" field')
def verify_field(context, value, field):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element_value((By.ID, field_id(field)), value)
    )
    assert found


@when('I copy the "{field}" field')
def copy_field(context, field):
    context.clipboard = context.driver.find_element(By.ID, field_id(field)).get_attribute("value")
    assert context.clipboard


@when('I paste the "{field}" field')
def paste_field(context, field):
    target = context.driver.find_element(By.ID, field_id(field))
    target.clear()
    target.send_keys(context.clipboard)


@when('I press the "{button_name}" button')
def step_impl(context, button_name):
    """Click a button on the page"""
    button_id = button_name.lower().replace(" ", "-") + "-btn"
    button = WebDriverWait(
        context.driver, context.wait_seconds
    ).until(
        expected_conditions.element_to_be_clickable((By.ID, button_id))
    )
    button.click()


@then('I should see "{text_string}" in the results')
def step_impl(context, text_string):
    """Verify text is present in search results"""
    found = WebDriverWait(
        context.driver, context.wait_seconds
    ).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "search_results"), text_string
        )
    )
    assert found


@then('I should not see "{text_string}" in the results')
def step_impl(context, text_string):
    """Verify text is absent from search results"""
    WebDriverWait(
        context.driver, context.wait_seconds
    ).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "flash_message"), "Success"
        )
    )
    results = context.driver.find_element(By.ID, "search_results").text
    assert text_string not in results


@then('I should see the message "{message}"')
def step_impl(context, message):
    """Verify the expected status message"""
    found = WebDriverWait(
        context.driver, context.wait_seconds
    ).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "flash_message"), message
        )
    )
    assert found
