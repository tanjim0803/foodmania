import { Button } from "../components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { Separator } from "../components/ui/separator";
import LoginForm from "../components/auth/LoginForm";
import { Link } from "react-router-dom";
import Logo from "../components/shared/Logo";
import AuthBackgroundShape from "../components/auth/AuthBackgroundShape";

const Login = () => {
  return (
    <div className="relative flex h-auto min-h-screen items-center justify-center overflow-hidden px-4 py-10 sm:px-6 lg:px-8">
      {/* SVG Background Shape */}
      <div className="absolute inset-0 flex items-center justify-center -z-10 pointer-events-none">
        <AuthBackgroundShape />
      </div>

      <Card className="z-10 w-full gap-4 py-6 sm:max-w-xs shadow-xl backdrop-blur-sm bg-card/95">
        <CardHeader className="gap-6 px-6">
          <div>
            <Logo />
          </div>

          <div>
            <CardTitle className="text-2xl font-semibold">
              Sign in to FOODMANIA
            </CardTitle>
          </div>
        </CardHeader>

        <CardContent className="px-6">
          {/* Login Form */}
          <div className="space-y-4">
            <LoginForm />

            <p className="text-muted-foreground text-center text-sm">
              New on our platform?{" "}
              <Link
                to="/pages/auth/register"
                className="text-card-foreground hover:underline"
              >
                Create an account
              </Link>
            </p>

            <div className="flex items-center gap-4">
              <Separator className="flex-1" />
              <p className="text-base text-muted-foreground">or</p>
              <Separator className="flex-1" />
            </div>

            <Button variant="ghost" className="w-full">
              <Link to="#">Sign in with Google</Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Login;
