import interactions
from typing import Union

bot = interactions.Client('Token Here')

@bot.command(
    name = 'prompt', description = 'Create a prompt for users to assign roles', options= [
        interactions.Option(
            type = interactions.OptionType.CHANNEL,
            name = 'channel',
            description = 'The channel you wish to assign this prompt to',
            required = True
        ),
        interactions.Option(
            type = interactions.OptionType.STRING,
            name = 'colour',
            description = 'HEX colour for roles you want to assign to this prompt, use this OR emoji OR text',
            required = False
        ),
        interactions.Option(
            type = interactions.OptionType.STRING,
            name = 'emoji',
            description = 'Unicode emoji for roles you want to assign to this prompt, use this OR colour OR text',
            required = False
        ),
        interactions.Option(
            type = interactions.OptionType.STRING,
            name = 'text',
            description = 'Text snippet for roles you want to assign to this prompt, use this OR colour OR emoji',
            required = False
        ),
        interactions.Option(
            type = interactions.OptionType.STRING,
            name = 'title',
            description = 'Title for the prompt embed',
            required = False
        ),
        interactions.Option(
            type = interactions.OptionType.STRING,
            name = 'description',
            description = 'Description for the prompt embed',
            required = False
        ),
        interactions.Option(
            type = interactions.OptionType.STRING,
            name = 'placeholder',
            description = 'Placeholder for the roles dropdown menu',
            required = False
        ),
        interactions.Option(
            type = interactions.OptionType.STRING,
            name = 'image',
            description = 'Image URL for the prompt embed',
            required = False
        )
    ]
    
)
async def makeprompt(
    ctx: interactions.CommandContext,
    channel: interactions.Channel,
    colour: Union[str, bool] = False,
    emoji: Union[str, bool] = False,
    text: Union[str, bool] = False,
    title: Union[str, bool] = False,
    description: Union[str, bool] = False,
    placeholder: Union[str, bool] = False,
    image: Union[str, bool] = False
) -> None:
    if ctx.author.permissions.MANAGE_GUILD:
        if title or description or image:
            if not placeholder: placeholder = 'Select your roles!'
            GUILD = await ctx.get_guild()
            OPTIONS = [
                interactions.SelectOption(
                    label = f'Remove all',
                    value = f'remove',
                    emoji = {
                        'name': 'Negative',
                        'id': '956464861041283092'
                    }
                )
            ]

            if colour:
                HEX_VALUE = int(colour, 16)
                for role in await GUILD.get_all_roles():
                    if (role.color == HEX_VALUE) and (not role.managed):
                        OPTIONS.append(
                            interactions.SelectOption(
                                label = f'{role.name}',
                                value = f'{role.id}',
                                emoji = {
                                    'name': 'Role',
                                    'id': '956464860571529267'
                                }
                            )
                        )
                COMMANDS = interactions.ActionRow(
                    components = [
                        interactions.SelectMenu(
                            custom_id = 'colourmenu',
                            options = OPTIONS,
                            placeholder = f'{placeholder}',
                            max_values = len(OPTIONS)
                        )
                    ]
                )
            
            elif emoji:
                HEX_VALUE = 0
                if not description: description = f'{emoji} | Roles'
                else: description += f'\n{emoji} | Roles'
                for role in await GUILD.get_all_roles():
                    if (role.unicode_emoji == emoji) and (not role.managed):
                        OPTIONS.append(
                            interactions.SelectOption(
                                label = f'{role.name}',
                                value = f'{role.id}',
                                emoji = {
                                    'name': 'Role',
                                    'id': '956464860571529267'
                                }
                            )
                        )
                COMMANDS = interactions.ActionRow(
                    components = [
                        interactions.SelectMenu(
                            custom_id = 'emojimenu',
                            options = OPTIONS,
                            placeholder = f'{placeholder}',
                            max_values = len(OPTIONS)
                        )
                    ]
                )
            
            elif text:
                HEX_VALUE = 0
                if not description: description = f'{text.lower()} | Roles'
                else: description += f'\n{text.lower()} | Roles'
                for role in await GUILD.get_all_roles():
                    if (role.name.lower().startswith(text.lower())) and (not role.managed):
                        OPTIONS.append(
                            interactions.SelectOption(
                                label = f'{role.name}',
                                value = f'{role.id}',
                                emoji = {
                                    'name': 'Role',
                                    'id': '956464860571529267'
                                }
                            )
                        )
                COMMANDS = interactions.ActionRow(
                    components = [
                        interactions.SelectMenu(
                            custom_id = 'textmenu',
                            options = OPTIONS,
                            placeholder = f'{placeholder}',
                            max_values = len(OPTIONS)
                        )
                    ]
                )
            
            if len(OPTIONS) > 0 and len(OPTIONS) < 26:
                if title and description and image:
                    EMBED = interactions.Embed(
                        title = title,
                        description = description,
                        color = HEX_VALUE,
                        image = interactions.EmbedImageStruct(
                            url = image
                        )._json
                    )
                elif title and description:
                    EMBED = interactions.Embed(
                        title = title,
                        description = description,
                        color = HEX_VALUE
                    )
                elif image and description:
                    EMBED = interactions.Embed(
                        description = description,
                        color = HEX_VALUE,
                        image = interactions.EmbedImageStruct(
                            url = image
                        )._json
                    )
                elif image and title:
                    EMBED = interactions.Embed(
                        title = title,
                        color = HEX_VALUE,
                        image = interactions.EmbedImageStruct(
                            url = image
                        )._json
                    )
                elif image:
                    EMBED = interactions.Embed(
                        color = HEX_VALUE,
                        image = interactions.EmbedImageStruct(
                            url = image
                        )._json
                    )
                elif title:
                    EMBED = interactions.Embed(
                        title = title,
                        color = HEX_VALUE
                    )
                elif description:
                    EMBED = interactions.Embed(
                        description = description,
                        color = HEX_VALUE
                    )
                if emoji and not(text or colour):
                    EMBED.set_footer(
                        text = f'{emoji} | Roles'
                    )
                
                print(f'{EMBED._json}\n\n{COMMANDS._json}')
                await channel.send(embeds = [EMBED], components = COMMANDS)
                await ctx.send(ephemeral = True, content = 'Prompt created!')
            else:
                await ctx.send(ephemeral = True, content = 'There are either too many or no roles that match this colour')
        else:
            await ctx.send(ephemeral = True, content = 'Please provide atleast one of Title, Description & Image')
    else:
        await ctx.send(ephemeral = True, content = 'You need the Manage Guild permission to use this command')

@bot.component('colourmenu')
async def assignRoles(ctx: interactions.ComponentContext, _options: list):
    GUILD = await ctx.get_guild()
    REMOVED = []
    TOGGLED = []
    OPTIONS = [
        interactions.SelectOption(
            label = f'Remove all',
            value = f'remove',
            emoji = {
                'name': 'Negative',
                'id': '956464861041283092'
            }
        )
    ]
    HEX_VALUE = ctx.message.embeds[0].color
    PLACEHOLDER = (((ctx.message.components[0])['components'])[0])['placeholder']
    MEMBER = await GUILD.get_member(int(ctx.author.id))
    changes = ''

    for role in await GUILD.get_all_roles():
        if (role.color == HEX_VALUE) and (not role.managed):
            OPTIONS.append(
                interactions.SelectOption(
                    label = f'{role.name}',
                    value = f'{role.id}',
                    emoji = {
                        'name': 'Role',
                        'id': '956464860571529267'
                    }
                )
            )
            if (str(role.id) in _options) and ('remove' not in _options):
                TOGGLED.append(role)
            else:
                REMOVED.append(role)

    for role in TOGGLED:
        await MEMBER.add_role(
            role, ctx.guild_id
        )
        changes += f'<:Positive:956464860890288198> <@&{role.id}>\n'
    
    for role in REMOVED:
        await MEMBER.remove_role(
            role, ctx.guild_id
        )
        changes += f'<:Negative:956464861041283092> <@&{role.id}>\n'
    
    COMMANDS = interactions.ActionRow(
        components = [
            interactions.SelectMenu(
                custom_id = 'colourmenu',
                options = OPTIONS,
                placeholder = f'{PLACEHOLDER}',
                max_values = len(OPTIONS)
            )
        ]
    )

    if changes == '': changes = 'No changes made'

    if COMMANDS._json != ctx.message.components:
        await ctx.edit(embeds = ctx.message.embeds, components = COMMANDS)
    await ctx.send(ephemeral = True, content = changes)

@bot.component('emojimenu')
async def assignRoles(ctx: interactions.ComponentContext, _options: list):
    GUILD = await ctx.get_guild()
    REMOVED = []
    TOGGLED = []
    MEMBER = await GUILD.get_member(int(ctx.author.id))
    PLACEHOLDER = (((ctx.message.components[0])['components'])[0])['placeholder']
    EMOJI = ((ctx.message.embeds[0].description.rsplit('\n'))[len(ctx.message.embeds[0].description.rsplit('\n')) -1]).strip(' | Roles')
    OPTIONS = [
        interactions.SelectOption(
            label = f'Remove all',
            value = f'remove',
            emoji = {
                'name': 'Negative',
                'id': '956464861041283092'
            }
        )
    ]
    HEX_VALUE = 0
    changes = ''

    for role in await GUILD.get_all_roles():
        if (role.unicode_emoji == EMOJI) and (not role.managed):
            OPTIONS.append(
                interactions.SelectOption(
                    label = f'{role.name}',
                    value = f'{role.id}',
                    emoji = {
                        'name': 'Role',
                        'id': '956464860571529267'
                    }
                )
            )
            if (str(role.id) in _options) and ('remove' not in _options):
                TOGGLED.append(role)
            else:
                REMOVED.append(role)

    for role in TOGGLED:
        await MEMBER.add_role(
            role, ctx.guild_id
        )
        changes += f'<:Positive:956464860890288198> <@&{role.id}>\n'
    
    for role in REMOVED:
        await MEMBER.remove_role(
            role, ctx.guild_id
        )
        changes += f'<:Negative:956464861041283092> <@&{role.id}>\n'
    
    COMMANDS = interactions.ActionRow(
        components = [
            interactions.SelectMenu(
                custom_id = 'emojimenu',
                options = OPTIONS,
                placeholder = f'{PLACEHOLDER}',
                max_values = len(OPTIONS)
            )
        ]
    )

    if changes == '': changes = 'No changes made'

    if COMMANDS._json != ctx.message.components:
        await ctx.edit(embeds = ctx.message.embeds, components = COMMANDS)
    await ctx.send(ephemeral = True, content = changes)

@bot.component('textmenu')
async def assignRoles(ctx: interactions.ComponentContext, _options: list):
    GUILD = await ctx.get_guild()
    REMOVED = []
    TOGGLED = []
    MEMBER = await GUILD.get_member(int(ctx.author.id))
    PLACEHOLDER = (((ctx.message.components[0])['components'])[0])['placeholder']
    TEXT = ((ctx.message.embeds[0].description.rsplit('\n'))[len(ctx.message.embeds[0].description.rsplit('\n')) -1]).strip(' | Roles').lower()
    OPTIONS = [
        interactions.SelectOption(
            label = f'Remove all',
            value = f'remove',
            emoji = {
                'name': 'Negative',
                'id': '956464861041283092'
            }
        )
    ]
    HEX_VALUE = 0
    changes = ''

    for role in await GUILD.get_all_roles():
        if (role.name.lower().startswith(TEXT)) and (not role.managed):
            OPTIONS.append(
                interactions.SelectOption(
                    label = f'{role.name}',
                    value = f'{role.id}',
                    emoji = {
                        'name': 'Role',
                        'id': '956464860571529267'
                    }
                )
            )
            if (str(role.id) in _options) and ('remove' not in _options):
                TOGGLED.append(role)
            else:
                REMOVED.append(role)

    for role in TOGGLED:
        await MEMBER.add_role(
            role, ctx.guild_id
        )
        changes += f'<:Positive:956464860890288198> <@&{role.id}>\n'
    
    for role in REMOVED:
        await MEMBER.remove_role(
            role, ctx.guild_id
        )
        changes += f'<:Negative:956464861041283092> <@&{role.id}>\n'
    
    COMMANDS = interactions.ActionRow(
        components = [
            interactions.SelectMenu(
                custom_id = 'textmenu',
                options = OPTIONS,
                placeholder = f'{PLACEHOLDER}',
                max_values = len(OPTIONS)
            )
        ]
    )

    if changes == '': changes = 'No changes made'

    if COMMANDS._json != ctx.message.components:
        await ctx.edit(embeds = ctx.message.embeds, components = COMMANDS)
    await ctx.send(ephemeral = True, content = changes)

@bot.event
async def on_ready():
    print(bot.me.name)

bot.start()