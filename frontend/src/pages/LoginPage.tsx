// internal imports
import "../App.css";


const LoginPage = ({ loginUrl }: { loginUrl: string }) => {
  const login = () => {
    window.location.href = loginUrl;
  };

  return (
    <div className='App'>
      <button onClick={() => login()}>Log In</button>
    </div>
  );
};

export default LoginPage;
