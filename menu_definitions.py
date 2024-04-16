from Menu import Menu
import logging
from Option import Option

menu_logging = Menu('debug', 'Please select the logging level from the following:', [
    Option("Debugging", "logging.DEBUG"),
    Option("Informational", "logging.INFO"),
    Option("Error", "logging.ERROR")
])

menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add new instance", "add()"),
    Option("Delete existing instance", "delete()"),
    Option("List existing instances", "list_members()"),
    Option("Select existing instance", "select()"),
    Option("Update existing instance", "update()"),
    Option("Exit", "pass")
])

# options for adding a new instance
add_select = Menu('add select', 'Which type of object do you want to add?:', [
    Option("Departmet", "add_department()"),
    Option("Course", "add_course()"),
    Option("Section", "add_section()"),
    Option("Exit", "pass")
])

# options for deleting an existing instance
delete_select = Menu('delete select', 'Which type of object do you want to delete?:', [
    Option("Department", "delete_department()"),
    Option("Course", "delete_course()"),
    Option("Section", "delete_section()"),
    Option("Exit", "pass")
])

# options for listing the existing instances
list_select = Menu('list select', 'Which type of object do you want to list?:', [
    Option("Department", "list_department()"),
    Option("Course", "list_course()"), 
    Option("Section", "list_section()"),
    Option("Exit", "pass")
])

# options for testing the select functions
select_select = Menu('select select', 'Which type of object do you want to select:', [
    Option("Department", "print(select_order())"),
    Option("Course", "print(select_product())"),
    Option("Section", "print(select_order_item())"),
    Option("Exit", "pass")
])

# options for testing the update functions
update_select = Menu("update select", 'Which type of object do you want to update:', [
    Option("Department", "update_order()"),
    Option("Course", "update_product()"),
    Option("Section", "update_order_item"),
    Option("Exit", "pass")
])
