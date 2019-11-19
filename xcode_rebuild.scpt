on chooseMenuItem(theAppName, theMenuName, theMenuItemName)
    try
        -- Bring the target app to the front
        tell application theAppName
            activate
        end tell
 
        -- Target the app
        tell application "System Events"
            tell process theAppName
 
                -- Target the menu bar
                tell menu bar 1
 
                    -- Target the menu by name
                    tell menu bar item theMenuName
                        tell menu theMenuName
 
                            -- Click the menu item
                            click menu item theMenuItemName
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


chooseMenuItem("Xcode", "Product", "Run")
