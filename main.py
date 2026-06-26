import discord
from discord import app_commands
from discord.ext import commands
import datetime

# Налаштування прав для бота (щоб бачив користувачів та повідомлення)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Подія, коли бот успішно ввімкнувся
@bot.event
async def on_ready():
    print(f'🤖 Ескобар у мережі! Бот {bot.user.name} готовий до тесту.')
    try:
        # Реєструємо слейш-команди в Discord
        await bot.tree.sync()
        print("✅ Усі тест-команди синхронізовано з Discord!")
    except Exception as e:
        print(f"Помилка синхронізації: {e}")


# 1. 🎭 КОМАНДА ВИДАЧІ РОЛІ (/role)
@bot.tree.command(name="role", description="Видати роль користувачу")
@app_commands.checks.has_permissions(manage_roles=True)
async def role(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if role in member.roles:
        await interaction.response.send_message(f"❌ У користувача {member.mention} вже є роль {role.name}!", ephemeral=True)
    else:
        await member.add_roles(role)
        await interaction.response.send_message(f"🎭 Успішно! Користувачу {member.mention} видано роль **{role.name}**.")


# 2. 🤫 КОМАНДА МУТУ (/mute) - закриває чат і войси на вказаний час
@bot.tree.command(name="mute", description="Замутити користувача у чаті та войсах")
@app_commands.checks.has_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "Порушення правил"):
    duration = datetime.timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await interaction.response.send_message(f"🤫 {member.mention} закрив пельку в чатах та войсах на **{minutes} хв.** (Причина: {reason})")


# 3. 🚫 КОМАНДА КІКУ (/kick)
@bot.tree.command(name="kick", description="Вигнати користувача з сервера")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Порушення правил"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"💨 {member.mention} вилетів із сервера під сраку! (Причина: {reason})")


# 4. 🔨 КОМАНДА БАНУ (/ban) - банить на певну кількість годин
@bot.tree.command(name="ban", description="Забанити користувача на сервері на певну кількість годин")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, hours: int, reason: str = "Порушення правил"):
    await member.ban(reason=reason, delete_message_days=1)
    await interaction.response.send_message(f"🔨 Користувача {member.mention} забанено на **{hours} год.** без права повернення! (Причина: {reason})")


# 5. 🧹 КОМАНДА ОЧИЩЕННЯ ЧАТУ (/clear)
@bot.tree.command(name="clear", description="Очистити певну кількість повідомлень")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    # Спочатку надсилаємо приховану відповідь, щоб Discord не лагав під час видалення
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"🧹 Чат підметено! Видалено повідомлень: {len(deleted)}.", ephemeral=True)


# Перевірка на адмін-права (якщо команду клацає звичайний юзер без прав)
@role.error
@mute.error
@kick.error
@ban.error
@clear.error
async def permissions_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Ранг не дозволяє! У тебе немає потрібних прав для цієї команди.", ephemeral=True)


# === СЮДИ ВСТАВ СВІЙ СЕКРЕТНИЙ ТОКЕН БОТА (лапки залишай!) ===
bot.run("MTUxOTk4OTI5NTg3NDcwNzUxNg.GdmJ4j.SrkZYtfKSGpi67RtqOJ9AsZlFYHm--FEBzuW2w")
