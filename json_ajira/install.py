import frappe
import json
import os
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
    try:
        # Get the path to the custom fields JSON file in your app
        app_path = frappe.get_app_path('json_ajira')
        json_file_path = os.path.join(app_path, 'custom', 'custom_fields.json')

        # Check if the JSON file exists
        if not os.path.exists(json_file_path):
            frappe.throw(f"Custom fields JSON file not found at {json_file_path}")

        # Load the custom fields JSON
        with open(json_file_path, 'r') as f:
            custom_fields_data = json.load(f)

        # Create the custom fields using Frappe's built-in function
        create_custom_fields(custom_fields_data)

        # Commit the changes to the database
        frappe.db.commit()

        # Show success message
        frappe.msgprint("Custom fields created successfully during app installation!")

    except Exception as e:
        # Log the error and raise an exception
        frappe.log_error(message=f"Error in after_install: {str(e)}", title="Custom Fields Creation Error")
        frappe.throw(f"An error occurred while creating custom fields: {str(e)}")
