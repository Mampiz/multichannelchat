# Multi-Channel Chat User Manual

Welcome to the multi-channel chat user guide. This document will assist you in getting started with our multi-channel chat application, guiding you through the steps of server initialization, connecting clients, and using the chat commands.

## Getting Started

### Starting the Server

The first step to using the multi-channel chat is to start the server. This is a prerequisite for clients wishing to connect.

### Connecting Clients

Once the server is up and running, clients can connect to it by entering the server's IP address and the corresponding port. Subsequently, clients will be prompted to enter their username to proceed.

## Chat Channels

### Creating a Channel

If no channels exist, you can create one by typing the command `CREATE channel_name`, where `channel_name` is the desired name for your new channel.

### Changing Channels

If you're already in a channel and wish to switch to another, type the command `MOVE channel_name`, where `channel_name` is the name of the channel you wish to join.

## Additional Commands

Our multi-channel chat offers several other commands to enhance your chat experience:

- `CHANNELS`: Displays a list of all the available channels.
- `USERS`: Shows a list of the users in the channel from which the command is executed.
- `ALL`: Presents a list of all channels and the users present in each one.
- `DEL channel_name`: Deletes the specified channel, where `channel_name` is the name of the channel you want to remove.

## Private Messaging

If a client wishes to send a private message to another client, they can do so by executing the command `PRIV username message`, followed by the message they wish to send, where `username` is the recipient's username.

Thank you for using our multi-channel chat application. If you have any questions or need further assistance, please refer to this manual or contact our support team.
