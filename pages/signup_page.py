from .base_page import BasePage
from utils.config import config
from playwright.sync_api import expect
import re

class SignupPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        # --- LOKÁTORY ---
        self.mr_radio_button = self.page.get_by_role("radio", name="Mr.")
        self.name_field = self.page.get_by_role("textbox", name="Name *", exact=True)
        self.email_field = self.page.get_by_role("textbox", name="Email *", exact=True)
        self.password_field = self.page.get_by_role("textbox", name="Password *")
        self.first_name = self.page.get_by_role("textbox", name="First name *")
        self.last_name = self.page.get_by_role("textbox", name="Last name *")
        self.company = self.page.get_by_role("textbox", name="Company", exact=True)
        self.address = self.page.get_by_role("textbox", name="Address * (Street address, P.")
        self.state =self.page.get_by_role("textbox", name="State *")
        self.city = self.page.get_by_role("textbox", name="City * Zipcode *")
        self.zipcode =self.page.locator("#zipcode")
        self.mobile_number = self.page.get_by_role("textbox", name="Mobile Number *")
        self.create_account_button =self.page.get_by_role("button", name="Create Account")
        self.account_created = self.page.get_by_text("Account Created!")
        self.continue_button = self.page.get_by_role("link", name="Continue")

        # Lokátory pro select boxy
        self.day_select = self.page.locator("#days")
        self.month_select = self.page.locator("#months")
        self.year_select = self.page.locator("#years")
        self.country_select = self.page.get_by_label("Country *")

    def enter_account_information(self, name: str, email: str, password: str, day: str, month: str, year: str):
        self.click(self.mr_radio_button, name="Mr. radio button")
        self.expect_visible(self.name_field, name=name)
        self.expect_visible(self.email_field, name=email)
        self.fill(self.password_field, password, name="password")
        
        # Výběr data narození
        # select_option rovnou vybere hodnotu, není potřeba na to pak klikat
        self.LOG.info(f"Vybírám datum narození: {day} {month} {year}")
        self.day_select.select_option(day)
        self.month_select.select_option(month)
        self.year_select.select_option(year)

    def enter_address_information(self, first_name: str, last_name: str, company: str, address: str, country: str, state: str, city: str, zipcode: str, mobile_number: str):
        self.click(self.page.get_by_role("checkbox", name="Sign up for our newsletter!"))
        self.click(self.page.get_by_role("checkbox", name="Receive special offers from"))
        self.fill(self.first_name, first_name, name="First name")
        self.fill(self.last_name, last_name, name="Last name")
        self.fill(self.company, company, name="Company")
        self.fill(self.address, address, name="Address")
        self.country_select.select_option(country)
        self.fill(self.state, state, name="State")
        self.fill(self.city, city, name="City")
        self.fill(self.zipcode, zipcode, name="Zipcode")
        self.fill(self.mobile_number, mobile_number, name="Mobile number")
        self.click(self.create_account_button, name="Create account button")
        self.expect_visible(self.account_created, name="Account created")
        expect(self.page).to_have_url(re.compile("https://automationexercise.com/account_created"))
        self.click(self.continue_button, name="Continue button")
        expect(self.page).to_have_url(re.compile("https://automationexercise.com/"))
        self.LOG.info(f"Úspěšně přesměrováno na Home page.")









