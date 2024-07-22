import { Button } from "@/components/ui/button";

const Index = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] p-4 text-center">
      <h1 className="text-4xl font-bold mb-4">Welcome to GPT-Engineer-Enhanced</h1>
      <p className="text-xl mb-8">Start building your enhanced AI-powered applications here.</p>
      <Button size="lg">Get Started</Button>
    </div>
  );
};

export default Index;