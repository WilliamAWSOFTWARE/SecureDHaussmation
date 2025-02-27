const express = require('express');
const router = express.Router();
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

// Ruta protegida /dashboard
router.get('/dashboard', (req, res) => {
  // Si el token es válido, se pasa la información del usuario a la vista
  //console.log(req.user)
  res.render('dashboard', { user: req.user });
});

// Ruta protegida /familias
router.get('/familias', (req, res) => {
  // Si el token es válido, se pasa la información del usuario a la vista
  //console.log(req.user)
  res.render('familias', { user: req.user });
});
// Ruta protegida /personas
router.get('/personas', (req, res) => {
  // Si el token es válido, se pasa la información del usuario a la vista
  //console.log(req.user)
  res.render('personas', { user: req.user });
});
// Ruta protegida /visitantes
router.get('/visitantes', (req, res) => {
  // Si el token es válido, se pasa la información del usuario a la vista
  //console.log(req.user)
  res.render('visitantes', { user: req.user });
});

// Ruta protegida /config
router.get('/config', (req, res) => {
  // Si el token es válido, se pasa la información del usuario a la vista
  //console.log(req.user)
  res.render('config', { user: req.user });
});

// Ruta protegida /hist
router.get('/hist', (req, res) => {
  // Si el token es válido, se pasa la información del usuario a la vista
  //console.log(req.user)
  res.render('hist', { user: req.user });
});

// Ruta protegida /authentic
router.get('/authentic', (req, res) => {
  // Si el token es válido, se pasa la información del usuario a la vista
  //console.log(req.user)
  res.render('authentic', { user: req.user });
});

// Ruta protegida /qrcodes
router.get('/qrcodes', (req, res) => {
  // Si el token es válido, se pasa la información del usuario a la vista
  //console.log(req.user)
  res.render('qrcodes', { user: req.user });
});

// Ruta protegida /pr
router.get('/pr', (req, res) => {
  // Si el token es válido, se pasa la información del usuario a la vista
  //console.log(req.user)
  res.render('pr', { user: req.user });
});

// Ruta protegida /magtag
router.get('/magtag', (req, res) => {
  // Si el token es válido, se pasa la información del usuario a la vista
  //console.log(req.user)
  res.render('magtag', { user: req.user });
});


module.exports = router;
