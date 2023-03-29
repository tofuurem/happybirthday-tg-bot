def new_member(update, context):
    for member in update.message.new_chat_members:
        if member.username == 'happy_bithday_notify_bot':
            # save room to db
            update.message.reply_text('Welcome')