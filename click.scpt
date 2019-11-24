property locationName : "city"

on chooseMenuItem(theAppName, theMenuName, theMenuItemName, theMenuItemName2)
    try
        tell application "System Events"
            tell process theAppName
                tell menu bar 1
                    tell menu bar item theMenuName
                        tell menu theMenuName
                             tell menu item theMenuItemName
                                  tell menu theMenuItemName
                                       tell menu item theMenuItemName2
                                            click
                                       end tell
                                  end tell
                             end tell
                        end tell
                    end tell
                end tell
            end tell
        end tell
        return true
    on error
        return false
    end try
end chooseMenuItem

chooseMenuItem("Xcode", "Debug", "Simulate Location", "London, England")
delay(0.2)
chooseMenuItem("Xcode", "Debug", "Simulate Location", "city")