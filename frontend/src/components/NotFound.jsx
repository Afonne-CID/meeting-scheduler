import Header from "./Header";

const NotFound = () => (
    <div className="text-center mt-[5em] m-4">
      <Header />
      <h1 className="text-[6em] text-blue-500">404</h1>
      <h2 className="text-[2em] text-[#636363]">Page Not Found</h2>
      <p className="text-[#ababab]">
        The page you are looking for does not exist. It might have been moved or deleted.
      </p>
    </div>
)

export default NotFound;
