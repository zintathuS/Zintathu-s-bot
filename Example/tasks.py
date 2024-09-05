from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
import os
 
@task
def robot_spare_bin_python():
    browser.configure(slowmo=100)
    open_robot_order_website()
    orders = get_orders()
    output_dir = "output"  # Define your output directory
    os.makedirs(output_dir, exist_ok=True)
    fill_the_forms(orders, output_dir)
 
 
def open_robot_order_website():
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    page = browser.page()
    page.click("button:text('OK')")
 
 
def get_orders():
    """Downloads and reads the orders CSV file"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)
 
    tables = Tables()
    orders = tables.read_table_from_csv("orders.csv")
    return orders
 
 
def fill_the_forms(orders, output_dir):
    page = browser.page()
    for order in orders:
        pdf_path = fill_and_submit_form(page, order, output_dir)
        screenshot_path = os.path.join(output_dir, f"screenshot_{order['Head']}{order['Body']}.png")
        final_pdf_path = os.path.join(output_dir, f"final_receipt_{order['Head']}{order['Body']}.pdf")
        embed_screenshot_in_pdf(pdf_path, screenshot_path, final_pdf_path)
 
 
def fill_and_submit_form(page, order, output_dir):
    page.select_option("#head", str(order["Head"]))
    page.click(f"#id-body-{order['Body']}")  # body is selected via radio buttons
    page.fill("input[placeholder='Enter the part number for the legs']", str(order["Legs"]))
    page.fill("#address", order["Address"])
    page.click("#preview")
    page.click("#order")
 
    while not page.is_visible("#order-another"):
        page.click("#order")  # Keep clicking order if it fails
 
    # Save pdf
    receipt_pdf_path = os.path.join(output_dir, f"receipt_{order['Head']}{order['Body']}.pdf")
    page.pdf(path=receipt_pdf_path)
 
    screenshot_path = os.path.join(output_dir, f"screenshot_{order['Head']}{order['Body']}.png")
    page.screenshot(path=screenshot_path) #selector="img#right-side-image")
 
    page.click("#order-another")
    page.click("button:text('OK')")
 
    return receipt_pdf_path
 
 
def embed_screenshot_in_pdf(pdf_path, screenshot_path, output_pdf_path):
    pdf = PDF()
    # pdf.add_watermark_image_to_pdf(screenshot_path, pdf_path, output_pdf_path)
 
 
if __name__ == "__main__":
    robot_spare_bin_python()