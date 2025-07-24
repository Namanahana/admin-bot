import discord
from discord.ext import commands
from config import token  # Import the bot's token from configuration file
import re
import random
import requests

intents = discord.Intents.default()
intents.members = True  # Allows the bot to work with users and ban them
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Deteksi pola link
link_regex = r'https?://\S+|www\.\S+'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    # Hindari bot merespon pesan sendiri
    if message.author == bot.user:
        return

    # Cek apakah pesan mengandung link
    if re.search(link_regex, message.content):
        try:
            await message.author.ban(reason="Mengirim link tanpa izin.")
            await message.channel.send(f"{message.author.mention} telah dibanned karena mengirimkan link.")
        except discord.Forbidden:
            await message.channel.send("Aku tidak punya izin untuk ban user ini.")
        except Exception as e:
            await message.channel.send(f"Terjadi kesalahan: {str(e)}")

    await bot.process_commands(message)  # Jangan lupa ini supaya command tetap berfungsi

@bot.event
async def on_member_join(member):
    # Mengirim pesan ucapan selamat
    for channel in member.guild.text_channels:
        await channel.send(f'Selamat datang, {member.mention}!')

@bot.command()
async def start(ctx):
    await ctx.send("Hi! I'm a chat manager bot!")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("It is not possible to ban a user with equal or higher rank!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"User {member.name} was banned.")
    else:
        await ctx.send("This command should point to the user you want to ban. For example: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have sufficient permissions to execute this command.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("User not found.")

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    '''Setelah kita memanggil perintah bebek (duck), program akan memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command(name="quote")
async def quote(ctx):
    try:
        response = requests.get("https://zenquotes.io/api/random")
        data = response.json()
        quote_text = data[0]["q"]
        author = data[0]["a"]
        await ctx.send(f"💡 \"{quote_text}\"\n— *{author}*")
    except:
        await ctx.send("Gagal mengambil quote. 😢")

@bot.command(name="cat")
async def cat(ctx):
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()
        cat_url = data[0]['url']
        embed = discord.Embed(title="Meong~ 😺")
        embed.set_image(url=cat_url)
        await ctx.send(embed=embed)
    except:
        await ctx.send("Gagal mengambil gambar kucing. 😿")

@bot.command()
async def pilih(ctx):
    message = await ctx.send("Pilih:\n👍\n👎")
    await message.add_reaction("👍")
    await message.add_reaction("👎")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["👍", "👎"]

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)
        if str(reaction.emoji) == "👍":
            await ctx.send("TENGS! aku emang paling best")
        elif str(reaction.emoji) == "👎":
            await ctx.send("Makasih feedbacknya, nnti aku evaluasi😢!")
    except TimeoutError:
        await ctx.send("Waktu habis. Silakan coba lagi.")


@bot.command(name="info")
async def info(ctx):
    embed = discord.Embed(
        title="📌 Info Bot",
        description="Bot multifungsi yang bisa kasih password random, gambar bebek, kucing lucu, kutipan inspirasional, dan masih banyak lagi! 🐤🐱💬",
        color=discord.Color.purple()
    )
    embed.add_field(name="Prefix", value="`/`", inline=True)
    embed.add_field(name="Developer", value="Aku yang sigma itu 😏", inline=True)
    embed.add_field(name="Command yang tersedia", value="1. Memberikan informasi tentang perintah yang tersedia serta fungsinya `(/info)`\n2. Membuat password random `(/passw)`\n3. Mengirim gambar bebek `(/duck)`\n4. Mengirim gambar kucing `(/cat)`\n5. Mengirim quotes `(/quote)`\n5. Memilih emoji! `(/pilih)`", inline=False)
    embed.set_footer(text="Salam kebajikan")

    await ctx.send(embed=embed)

bot.run(token)