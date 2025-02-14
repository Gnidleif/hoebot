const { SlashCommandBuilder } = require("discord.js");

module.exports = {
    data: new SlashCommandBuilder()
        .setName("user")
        .setDescription("Provides information about user"),
    async execute(interaction) {
        await interaction.reply(`Run by: ${interaction.user.username}, who joined on ${interaction.member.joinedAt}`);
    },
}