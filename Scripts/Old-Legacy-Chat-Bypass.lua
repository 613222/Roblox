local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")
local DefaultChatSystemChatEvents = ReplicatedStorage:WaitForChild("DefaultChatSystemChatEvents")
local function replace(msg, replacementarray)
	local new_message = ""
	for i = 1, #msg do
		local char = string.sub(msg, i, i)
		if replacementarray[char] ~= nil then
			new_message = new_message .. replacementarray[char] .. "\226\129\165"
		else
			new_message = new_message .. char .. "\226\129\165"
		end
	end
	return new_message
end
local replacements = {
	["A"] = "\208\144",
	["a"] = "\208\176",
	["B"] = "\208\146",
	["C"] = "\208\161",
	["c"] = "\209\129",
	["E"] = "Е",
	["e"] = "е",
	["g"] = "⁥g⁥",
	["H"] = "Н",
	["I"] = "І",
	["i"] = "і",
	["J"] = "Ј",
	["j"] = "ј",
	["M"] = "М",
	["N"] = "Ν",
	["O"] = "О",
	["o"] = "о",
	["P"] = "Р",
	["p"] = "р",
	["S"] = "Ѕ",
	["s"] = "ѕ",
	["T"] = "Т",
	["U"] = "U",
	["u"] = "⁥u⁥",
	["X"] = "Х",
	["x"] = "х",
	["Y"] = "Ү",
	["y"] = "у",
	["Z"] = "Ζ",
	[" "] = "\30",
	["GG"] = "￰GG",
	["gg"] = "￰gg",
}
local syntax = true
local function makestr(message)
	local new_message = replace(message, replacements)
	local final = "\217\156\32\217\156\32\217\156\32\217\156\32\30\239\191\176\83\65\88\239\191\176\30" .. new_message .. "\32\225\128\173"
	return final
end
local function say(msg)
	if syntax then
		DefaultChatSystemChatEvents.SayMessageRequest:FireServer(makestr(msg), "All")
	else
		DefaultChatSystemChatEvents.SayMessageRequest:FireServer(msg, "All")
	end
end
local Chat = Instance.new("ScreenGui")
local Frame = Instance.new("Frame")
local Title = Instance.new("TextLabel")
local Toggle = Instance.new("TextButton")
local TextBox = Instance.new("TextBox")
local Send = Instance.new("TextButton")
Chat.Name = "ChatBypass"
Chat.Parent = game:GetService("CoreGui")
Frame.Parent = Chat
Frame.Active = true
Frame.Draggable = true
Frame.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
Frame.BorderColor3 = Color3.fromRGB(0, 0, 0)
Frame.Position = UDim2.new(0, 4, 0, 4)
Frame.Size = UDim2.new(0, 150, 0, 200)
Title.Name = "Title"
Title.Parent = Frame
Title.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
Title.BorderColor3 = Color3.fromRGB(0, 0, 0)
Title.Size = UDim2.new(0, 150, 0, 30)
Title.Font = Enum.Font.Gotham
Title.Text = "C.B | 613222"
Title.TextColor3 = Color3.fromRGB(0, 0, 0)
Title.TextScaled = true
Title.TextSize = 14.000
Title.TextWrapped = true
Toggle.Name = "Toggle"
Toggle.Parent = Frame
Toggle.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
Toggle.BorderColor3 = Color3.fromRGB(0, 0, 0)
Toggle.Position = UDim2.new(0.0799999982, 0, 0.219999999, 0)
Toggle.Size = UDim2.new(0, 125, 0, 37)
Toggle.Font = Enum.Font.GothamBold
Toggle.Text = "Enabled"
Toggle.TextColor3 = Color3.fromRGB(0, 0, 0)
Toggle.TextSize = 18.000
Toggle.MouseButton1Click:Connect(function()
	if syntax then
		syntax = false
		Toggle.Text = "Disabled"
	else
		syntax = true
		Toggle.Text = "Enabled"
	end
end)
TextBox.Parent = Frame
TextBox.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
TextBox.BorderColor3 = Color3.fromRGB(0, 0, 0)
TextBox.Position = UDim2.new(0.0799999982, 0, 0.474999994, 0)
TextBox.Size = UDim2.new(0, 125, 0, 40)
TextBox.ClearTextOnFocus = false
TextBox.Font = Enum.Font.Gotham
TextBox.PlaceholderText = "String"
TextBox.Text = ""
TextBox.TextColor3 = Color3.fromRGB(0, 0, 0)
TextBox.TextSize = 12.000
TextBox.TextWrapped = true
Send.Name = "Send"
Send.Parent = Frame
Send.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
Send.BorderColor3 = Color3.fromRGB(0, 0, 0)
Send.Position = UDim2.new(0.0799999982, 0, 0.74000001, 0)
Send.Size = UDim2.new(0, 125, 0, 37)
Send.Font = Enum.Font.GothamBold
Send.Text = "Send Message"
Send.TextColor3 = Color3.fromRGB(0, 0, 0)
Send.TextSize = 18.000
Send.MouseButton1Click:Connect(function()
	say(TextBox.Text)
end)
