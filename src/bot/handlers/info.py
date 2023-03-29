
@inject
async def _users_info(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    """
    Returns info about user and their birthdays

    like:
        user1: 22.10.1987
        user2: 10.12.1934

    :param update:
    :param context:
    :return:
    """
    data = await cache.all_chat_str('*_{}'.format(update.effective_chat.id))
    if not data:
        text = 'No data about users in this chat'
    else:
        text = f" All users with birthdays:\n{data}"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode='HTML'
    )

