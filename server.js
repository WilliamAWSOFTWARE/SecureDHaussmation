const express = require("express");
const path = require("path");
//const verifyToken = require("./src/middlewares/auth.js"); // Importa el middleware de verificación de token
const app = express();
const port = 3000;
const sqlrouter = require('./src/sql/auth');
const apiRoutes = require('./src/routes/routes'); // Importa el archivo de rutas

// Configurar EJS como motor de vistas
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "./src/views"));
app.use('/image', express.static(path.join(__dirname, './src/images')))

//Custom JS and CSS
app.use('/css', express.static(path.join(__dirname, './dashboard/css')))
app.use('/icons', express.static(path.join(__dirname, './node_modules/bootstrap-icons/font')))
app.use('/js', express.static(path.join(__dirname, './dashboard/js')))
app.use('/jss', express.static(path.join(__dirname, './node_modules')))

// Middleware para parsear el body de las solicitudes
app.use(express.json()); // Para procesar datos JSON
app.use(express.urlencoded({ extended: true })); // Para procesar datos con formato de formulario
app.use(sqlrouter);
app.use(apiRoutes); // Usa las rutas'

// Ruta para mostrar la vista de login

app.get('/', (req, res) => {
  res.render("login");
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`🚀 Servidor corriendo en http://localhost:${port}`);
});
