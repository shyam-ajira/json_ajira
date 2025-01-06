import frappe

def before_uninstall():
    try:
        # Fields to drop from tabLead table
        fields_to_drop = [
            "district", "municipality", "ward", "unit_type", 
            "ropani", "aana", "paisa", "daam", 
            "bigha", "kattha", "dhur", "sq_feet", "sq_mtr"
        ]

        table_name = "tabLead"

        # Direct SQL to check if table exists
        table_exists = frappe.db.sql(f"SHOW TABLES LIKE '{table_name}'")
        
        if table_exists:
            # Drop columns directly using SQL
            for field in fields_to_drop:
                frappe.db.sql(f"ALTER TABLE `{table_name}` DROP COLUMN IF EXISTS `{field}`")
                frappe.msgprint(f"Dropped column: {field} from {table_name}")

        # Delete custom fields from Frappe's Custom Field doctype
        custom_fields = frappe.get_all("Custom Field", filters={"dt": "Lead"})
        for field in custom_fields:
            frappe.delete_doc("Custom Field", field.name, force=True)

        frappe.msgprint("Custom fields and columns deleted successfully.")

    except Exception as e:
        frappe.log_error(message=f"Error in before_uninstall: {str(e)}", title="Uninstall Error")
        frappe.throw(f"An error occurred while deleting custom fields and columns: {str(e)}")
