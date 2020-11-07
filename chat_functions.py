from selenium.webdriver.common.keys import Keys

sent = []

def repeated_chat(texts, n):
    count = 0
    all_chats = " ".join(texts)
    for text in texts[-10:]:
        count = all_chats.count(text)
        if count >= n:
            return text
    return ""


def chat_bot(driver):
    # text = input("Nadaljuj?")
    # if text == "n":
    #     break

    # find chats and make a list of chats
    chat_elements = driver.find_elements_by_xpath(
        "//pre[@class=\"chat-item__chat-info-msg\"]")
    chats = [chat.text for chat in chat_elements]

    global sent
    
    if len(chats) > 0:
        # get the word that repeated specified number of times
        text = repeated_chat(chats, 3)

        if text and text not in sent:
            print("Found >=3 chats")
            # get textbox and send the repeated chat
            chatbox = driver.find_element_by_xpath(
                "//textarea[@class=\"chat-box__chat-textarea\"]")
            chatbox.send_keys(text)
            chatbox.send_keys(Keys.RETURN)
            sent.append(text)
