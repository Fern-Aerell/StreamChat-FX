import { Socket, io } from 'socket.io-client';

export enum ChatType {
    Default = 'default',
}

export interface Chat {
    type: ChatType;
    name: string;
    message: string;
}

export class LevaYTLiveChatClient {
    private hostname: string;
    private port: number;
    private io: Socket | null;

    constructor(port: number) {
        this.hostname = 'localhost';
        this.port = port;
        this.io = null;
    }

    connect(): void {
        if (!this.io) {
            this.io = io(`http://${this.hostname}:${this.port}`);
        } else {
            console.warn("Socket is already connected.");
        }
    }

    listen(callback: (data: Chat) => void): void {
        if (this.io) {
            this.io.on('latest-chat', callback);
        } else {
            console.error("Socket is not connected. Call connect() first.");
        }
    }

    unlisten(callback: (data: Chat) => void): void {
        if (this.io) {
            this.io.off('latest-chat', callback);
        } else {
            console.error("Socket is not connected. Call connect() first.");
        }
    }

    shutdown(): void {
        if (this.io) {
            this.io.disconnect();
            this.io = null;
        } else {
            console.warn("Socket is already disconnected.");
        }
    }
}