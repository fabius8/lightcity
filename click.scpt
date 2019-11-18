property locationName : "city"

tell application "System Events"
	tell process "Xcode"
		click menu item "London, England" of menu 1 of menu item "Simulate Location" of menu 1 of menu bar item "Debug" of menu bar 1
		delay 0.2
		click menu item locationName of menu 1 of menu item "Simulate Location" of menu 1 of menu bar item "Debug" of menu bar 1
	end tell
end tell
