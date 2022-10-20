

@inject
async def _fullness_check(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache: Cache = Provide[Container.cache]
) -> None:
    """
    Check that count users in chat equals users in cache
    :param update:
    :param context:
    :return:
    """
    # ToDo: get only users without bots
    member_count = await update.effective_chat.get_member_count()
    users = [u for u in await cache.dall_users() if u.group_id == update.effective_chat.id]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Statistic {}/{} (reg member with birthday/members in chat)".format(len(users), member_count)
    )

