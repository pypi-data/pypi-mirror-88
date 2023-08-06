from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices


# Declare a list of menu items to be added to NetBox's built-in naivgation menu
menu_items = (

    # Each PluginMenuItem instance renders a custom menu item. Each item may have zero or more buttons.
   
    PluginMenuItem(
        link='plugins:conectividadeapp:actor_list',
        link_text='Actors',
        permissions=[],
        buttons=(
            PluginMenuButton(
                link='plugins:conectividadeapp:addactor',
                title='Add a new actor',
                icon_class='fa fa-plus',
                color=ButtonColorChoices.GREEN,
                permissions=[]
            ),
        )
    ),
    PluginMenuItem(
        link='plugins:conectividadeapp:activity_list',
        link_text='Activities',
        permissions=[],
        buttons=(
             # Add a default button which links to the random animal view
            PluginMenuButton(
                link='plugins:conectividadeapp:searchdevice',
                title='searchdevice and activity',
                icon_class='fa fa-question'
            ),

            # Add a green button which links to the admin view to add a new animal. This
            # button will appear only if the user has the "add_animal" permission.
            PluginMenuButton(
                link='plugins:conectividadeapp:list',
                title='Add a new activity for the last device',
                icon_class='fa fa-plus',
                color=ButtonColorChoices.GREEN,
                permissions=[]
            ),
        ),
    ),   
)