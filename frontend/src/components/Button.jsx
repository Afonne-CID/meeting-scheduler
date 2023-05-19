import { funcType, nodeType, stringType } from '../utils/propTypes';

const Button = ({ onClick, children, color, hoverColor, extraClasses }) => {
  const baseClasses = `font-bold py-2 px-4 rounded 
                      focus:outline-none focus:shadow-outline
                      `;
  const colorClasses = `bg-${color} hover:bg-${hoverColor} text-white`;
  return (
    <button 
      onClick={onClick} 
      className={`${baseClasses} ${colorClasses} ${extraClasses}`}
    >
      {children}
    </button>
  );
};

Button.propTypes = {
    onClick: funcType,
    children: nodeType.isRequired,
    color: stringType,
    hoverColor: stringType,
    extraClasses: stringType,
};

Button.defaultProps = {
  color: "blue-500",
  hoverColor: "blue-700",
  extraClasses: "",
};

export default Button;
