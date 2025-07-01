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


# 역할 ID 설정
ROLE_IDS = {
    "여자": 1381621262312538258,  # 예: @여자 역할 ID
    "남자": 1381621262312538257,  # 예: @남자 역할 ID
    "10대": 1381621262312538256,  # 예: @10대 역할 ID
    "20대": 1381621262312538255,  # 예: @20대 역할 ID
}

# 항상 같이 부여되는 기본 역할들 (선택 사항)
DEFAULT_ROLE_IDS = [
    1381621262312538261,  # 예: @주인님
    1381621262312538262,  # 예: @첫손님
]

# 로그를 남길 채널 ID
LOG_CHANNEL_ID = 1381621262874574884  # 로그 채널 ID로 바꿔줘


@bot.command()
async def 역할지급(ctx, member: discord.Member, gender: str, birth_year: str, path: str):
    valid_genders = ["여자", "남자"]

    # 생년 숫자로 변환
try:
    birth_year = int(birth_year)
    if birth_year >= 100:
        birth_year = birth_year % 100  # 2000년대생 처리
    birth_year_full = 2000 + birth_year if birth_year < 100 else birth_year
except ValueError:
    await ctx.send("❗생년은 숫자(예: 08, 06)로 입력해주세요.")
    return

# 현재 연도에서 생년 빼기 → 나이 계산
current_year = datetime.now().year
age = current_year - birth_year_full

# 나이 기반 그룹 지정
if 10 <= age <= 19:
    age_group = "10대"
elif 20 <= age <= 29:
    age_group = "20대"
else:
    await ctx.send(f"⚠️ `{age}세`는 10대/20대 범위가 아니에요.")
    return

    gender_role = ctx.guild.get_role(ROLE_IDS.get(gender))
    age_role = ctx.guild.get_role(ROLE_IDS.get(age_group))
    default_roles = [ctx.guild.get_role(rid) for rid in DEFAULT_ROLE_IDS]

    all_roles = [r for r in [gender_role, age_role] + default_roles if r]

    if not gender_role or not age_role:
        await ctx.send("❗역할을 찾을 수 없습니다. ROLE_IDS 값을 확인해주세요.")
        return

    try:
        await member.add_roles(*all_roles)
        role_names = ', '.join(role.name for role in all_roles)
        await ctx.send(f"✅ {member.mention}님에게 `{role_names}` 역할이 지급되었어요!")

        # 로그 전송
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"📌 **역할지급 기록**\n"
                f"👤 대상: {member.mention}\n"
                f"⚧ 성별: `{gender}`\n"
                f"📅 생년: `{birth_year}년생` → `{age_group}`\n"
                f"🛤 경로: `{path}`\n"
                f"🎖 부여된 역할: `{role_names}`\n"
                f"🕒 처리자: {ctx.author.mention}"
            )

    except discord.Forbidden:
        await ctx.send("🚫 역할을 부여할 권한이 없어요.")
    except discord.HTTPException as e:
        await ctx.send(f"⚠️ 역할 지급 중 오류가 발생했어요: `{e}`")


@역할지급.error
async def 역할지급_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❗사용법: `!역할지급 @유저 (남자/여자) (생년) (경로)`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❗올바른 유저를 멘션했는지 확인해주세요.")
    else:
        await ctx.send(f"⚠️ 오류 발생: {error}")

bot.run(os.environ['TOKEN1']) 
