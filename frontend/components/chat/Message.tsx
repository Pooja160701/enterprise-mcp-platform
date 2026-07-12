interface Props {

    role: "user" | "assistant";

    content: string;

}

export default function Message({

    role,

    content,

}: Props) {

    return (

        <div

            className={`mb-6 flex ${role === "user"

                ? "justify-end"

                : "justify-start"

                }`}

        >

            <div

                className={`max-w-2xl rounded-2xl p-5

${role === "user"

                        ? "bg-blue-600 text-white"

                        : "bg-zinc-800 text-zinc-100"

                    }

`}

            >

                {content}

            </div>

        </div>

    );

}