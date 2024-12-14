class LevaYTLiveChatClient {
    constructor(hostname, port) {
        this.hostname = hostname;
        this.port = port;
        this.io = null;
    }

    connect() {
        if (!this.io) {
            this.io = io(`http://${this.hostname}:${this.port}`);
        } else {
            console.warn("Socket is already connected.");
        }
    }

    listen(callback) {
        if (this.io) {
            this.io.on('latest-chat', callback);
        } else {
            console.error("Socket is not connected. Call connect() first.");
        }
    }

    unlisten(callback) {
        if (this.io) {
            this.io.off('latest-chat', callback);
        } else {
            console.error("Socket is not connected. Call connect() first.");
        }
    }

    shutdown() {
        if (this.io) {
            this.io.disconnect();
            this.io = null;
        } else {
            console.warn("Socket is already disconnected.");
        }
    }
}