const jwt = require('jsonwebtoken');
const SECRET_KEY = "jardines"; // Usa tu clave secreta aquí

// Middleware para verificar el token JWT
const verifyToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];

    //console.log("Token recibido en el backend:", authHeader); // Debe imprimir: "Bearer <token>"
  
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return res.status(403).json({ error: "No token provided o formato incorrecto" });
    }
  
    // Extraer el token real
    const token = authHeader.split(" ")[1];
    //console.log("Token limpio:", token); // Debe mostrar solo el token sin "Bearer"
  
    jwt.verify(token, SECRET_KEY, (err, decoded) => {
      if (err) {
        console.log("Error en la verificación del token:", err.message);
        return res.status(401).json({ error: "Token no válido o expirado" });
      }
  
      console.log("Token verificado con éxito:", decoded); // Debe mostrar los datos del usuario
  
      req.user = decoded; // Guardar el usuario decodificado en la petición
      next();
    });
  };
  
  

module.exports = verifyToken;
