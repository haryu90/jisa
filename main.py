from keep_alive import keep_alive

keep_alive()

import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 역할 이름 ➡ 역할 ID 매핑
ROLE_IDS = {
    "여자": 1381621262312538258,  # 실제 ID로 변경!
    "남자": 1381621262312538257,
    "10대": 1381621262312538256,
    "20대": 1381621262312538255,
}

DEFAULT_ROLE_IDS = [
    1381621262312538261,  # 주인님 역할 ID
    1381621262312538262,  # 첫손님 역할 ID
]


@bot.event
async def on_ready():
    print(f"✅ 봇이 로그인되었습니다: {bot.user}")
    activity = discord.Game(name="메이드랑 주인님 대접하는 중")
    await bot.change_presence(status=discord.Status.online, activity=activity)


def has_role_id(role_id: int):

    def predicate(ctx):
        role = discord.utils.get(ctx.author.roles, id=role_id)
        return role is not None

    return commands.check(predicate)


# 예시 역할 ID (실제 역할 ID로 바꿔주세요)
운영진_역할_ID = 1381184295598821447


@bot.command()
async def 이름(ctx, member: discord.Member, *, new_name: str):
    formatted_name = f"『🤍』︰{new_name} ꒷꒦₊"
    try:
        await member.edit(nick=formatted_name)
        await ctx.send(
            f"✨ {member.mention} 님의 닉네임이 `{formatted_name}` 으로 변경되었어요!")
    except discord.Forbidden:
        await ctx.send("🚫 닉네임을 변경할 수 있는 권한이 없어요.")
    except discord.HTTPException as e:
        await ctx.send(f"⚠️ 닉네임 변경 중 오류: `{e}`")


@이름.error
async def 이름_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❗사용법: `!이름 @유저 새이름` 형식으로 입력해주세요!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❗올바른 유저를 멘션했는지 확인해주세요!")
    else:
        await ctx.send(f"⚠️ 오류 발생: {error}")


@bot.command()
async def 역할지급(ctx, member: discord.Member, gender: str, age_group: str):
    valid_genders = ["여자", "남자"]
    valid_ages = ["10대", "20대"]

    if gender not in valid_genders or age_group not in valid_ages:
        await ctx.send("❗사용법: `!역할지급 @유저 (여자/남자) (10대/20대)`")
        return

    gender_role = ctx.guild.get_role(ROLE_IDS.get(gender))
    age_role = ctx.guild.get_role(ROLE_IDS.get(age_group))
    default_roles = [
        ctx.guild.get_role(role_id) for role_id in DEFAULT_ROLE_IDS
    ]

    # 모든 역할 합치기
    all_roles = [r for r in [gender_role, age_role] + default_roles if r]

    if not gender_role or not age_role:
        await ctx.send("❗선택한 성별/나이 역할이 존재하지 않아요.")
        return

    try:
        await member.add_roles(*all_roles)
        role_names = ', '.join([role.name for role in all_roles])
        await ctx.send(f"✅ {member.mention}님에게 `{role_names}` 역할이 지급되었어요!")
    except discord.Forbidden:
        await ctx.send("🚫 역할을 부여할 권한이 없어요.")
    except discord.HTTPException as e:
        await ctx.send(f"⚠️ 역할 지급 중 오류가 발생했어요: `{e}`")


@역할지급.error
async def 역할지급_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❗사용법: `!역할지급 @유저 (여자/남자) (10대/20대)`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❗올바른 유저를 멘션했는지 확인해주세요.")
    else:
        await ctx.send(f"⚠️ 오류 발생: {error}")


bot.run(os.environ['TOKEN1'])
