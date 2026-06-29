import ReactMarkdown from "react-markdown";

type Props = {
  role: "user" | "assistant";
  message: string;
};

export default function MessageBubble({
  role,
  message,
}: Props) {
  const isUser = role === "user";

  return (
    <div
      className={`flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-[75%] rounded-2xl px-5 py-4 text-sm leading-7 ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-zinc-900 text-zinc-100"
        }`}
      >
        {isUser ? (
          message
        ) : (
          <ReactMarkdown
            components={{
              h1: ({ children }) => (
                <h1 className="text-2xl font-bold mt-4 mb-3">
                  {children}
                </h1>
              ),

              h2: ({ children }) => (
                <h2 className="text-xl font-semibold mt-4 mb-2">
                  {children}
                </h2>
              ),

              h3: ({ children }) => (
                <h3 className="text-lg font-semibold mt-3 mb-2">
                  {children}
                </h3>
              ),

              p: ({ children }) => (
                <p className="mb-3">
                  {children}
                </p>
              ),

              ul: ({ children }) => (
                <ul className="list-disc ml-6 mb-3">
                  {children}
                </ul>
              ),

              ol: ({ children }) => (
                <ol className="list-decimal ml-6 mb-3">
                  {children}
                </ol>
              ),

              li: ({ children }) => (
                <li className="mb-1">
                  {children}
                </li>
              ),

              strong: ({ children }) => (
                <strong className="font-bold">
                  {children}
                </strong>
              ),

              em: ({ children }) => (
                <em className="italic">
                  {children}
                </em>
              ),

              code: ({ children }) => (
                <code className="rounded bg-zinc-800 px-1 py-0.5">
                  {children}
                </code>
              ),
            }}
          >
            {message}
          </ReactMarkdown>
        )}
      </div>
    </div>
  );
}