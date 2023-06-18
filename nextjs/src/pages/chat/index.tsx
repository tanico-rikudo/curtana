"use client";
import { ReactElement, useEffect, useState } from "react";

import type { NextPageWithLayout } from "./_app";
import Container from "@/components/containers/index";
import Layout from "@/components/templates/Layout";
import { useSession } from "next-auth/react";

type Message = {
    userId: number;
    text: string;
};

const ChatHome: NextPageWithLayout = () => {
    return (
        <Container>
            <div>{renderChatBoard()}</div>
        </Container>
    );
};

ChatHome.getLayout = function getLayout(page: ReactElement) {
    return <Layout>{page}</Layout>;
};


const renderChatBoard = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const { data: session } = useSession();


    const sendMessage = (e: { preventDefault: () => void }) => {
        e.preventDefault();

        if (input !== "") {
            messages.push({ userId: 0, text: input });
            setMessages([...messages]);
            fetch(`api/gpt`, {
                method: "POST",
                headers: {
                    "content-type": "application/json;charset=UTF-8",
                },
                body: JSON.stringify({
                    prompt: input,
                }),
            }).then(async (data) => {
                const result = await data.json();
                console.log(result.message)
                messages.push({
                    userId: 1,
                    text: result.message.content || "sorry not response gpt",
                });
                setMessages([...messages]);
            });
            setInput("");
        }
    };

    return (
        <>
            <div className="flex flex-col h-screen bg-brack-100">
                <div className="flex flex-row justify-center items-center bg-slate-950 p-4">
                    <h1 className="text-white text-2xl">ChatGPT App</h1>
                </div>
                <div className="flex flex-col flex-grow overflow-y-scroll  bg-slate-900">
                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`flex flex-row ${message.userId === 0 ? "justify-end" : "justify-start"
                                } items-end p-4`}
                        >
                            <p
                                className={`max-w-xs text-white ${message.userId === 0 ? "bg-slate-500" : "bg-slate-500"
                                    } rounded-lg p-2 mb-2`}
                            >
                                {message.text}
                            </p>
                        </div>
                    ))}
                </div>
                <form
                    onSubmit={sendMessage}
                    className="flex flex-row items-center p-4 bg-slate-950">
                    <input
                        value={input}
                        disabled={session === null}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder={session === null ? "Please login to chat" : "Type your message here"}
                        className="flex-grow rounded p-2 mr-4 bg-slate text-white" />
                    <button
                        type="submit"
                        disabled={session === null}
                        className="bg-slate-800 text-white rounded p-2">
                        Send
                    </button>
                </form>
            </div>
        </>
    );
};

export default ChatHome;