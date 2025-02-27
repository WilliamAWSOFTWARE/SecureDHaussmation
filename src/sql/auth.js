const express = require("express");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const connection = require("../configs/db");

const router = express.Router();
const SECRET_KEY = process.env.SECRET_KEY || "jardines"; // 🔒 Asegúrate de usar una clave más segura en producción

// ✅ REGISTRO DE USUARIOS
router.post("/register", async (req, res) => {
  const { usuario, password } = req.body;

  // Validar que los datos no estén vacíos
  if (!usuario || !password) {
    return res.status(400).json({ error: "Todos los campos son obligatorios" });
  }

  try {
    // Encriptar la contraseña
    const hashedPassword = await bcrypt.hash(password, 10);

    // Insertar el usuario en la base de datos
    const [results] = await connection.query("INSERT INTO usuarios (username, password) VALUES (?, ?)", [
      usuario,
      hashedPassword,
    ]);

    res.status(201).json({ message: "Usuario registrado con éxito" });
  } catch (error) {
    console.error("Error al registrar usuario:", error);
    res.status(500).json({ error: "Error al registrar usuario" });
  }
});

// ✅ LOGIN DE USUARIOS
router.post("/login", async (req, res) => {
  try {
      const { username, password } = req.body;

      // Verificar si el usuario existe en la base de datos
      const [rows] = await connection.query(
          "SELECT id, username, password, tipo_usuario FROM usuarios WHERE username = ? AND activo = 1",
          [username]
      );

      if (rows.length === 0) {
          return res.status(401).json({ message: "Usuario no encontrado" });
      }

      const user = rows[0];

      // Comparar la contraseña ingresada con la almacenada en la base de datos
      const passwordMatch = await bcrypt.compare(password, user.password);
      if (!passwordMatch) {
          return res.status(401).json({ message: "Contraseña incorrecta" });
      }

      // Crear el token JWT
      const token = jwt.sign(
          { id: user.id, username: user.username, tipo_usuario: user.tipo_usuario },
          SECRET_KEY,
          { expiresIn: "2h" }
      );

      res.json({ message: "Login exitoso", token });
  } catch (error) {
      console.error("Error en el login:", error);
      res.status(500).json({ message: "Error interno del servidor" });
  }
});






// ✅ OBTENER DATOS DE LA TABLA FAMILIA
router.get("/familias_t", async (req, res) => {
  try {
    const [rows] = await connection.query("SELECT * FROM familias");
    res.json(rows);
  } catch (error) {
    console.error("Error al obtener datos de familias:", error);
    res.status(500).json({ error: "Error al obtener datos de la base de datos" });
  }
});
// ✅ AGREGAR A LA TABLA FAMILIA
router.post("/agregar-familia", async (req, res) => {
  const { codigo, nombreFamilia, representante, direccion, telefono } = req.body;

  if (!codigo || !nombreFamilia || !representante || !direccion || !telefono) {
      return res.status(400).json({ error: "Todos los campos son obligatorios" });
  }

  try {
      const [result] = await connection.query(
          "INSERT INTO familias (codigo_familia, nombre_familia, representante, direccion, telefono) VALUES (?, ?, ?, ?, ?)",
          [codigo, nombreFamilia, representante, direccion, telefono]
      );

      res.status(201).json({ message: "Familia agregada correctamente", id: result.insertId });
  } catch (error) {
      console.error("Error al agregar familia:", error);
      res.status(500).json({ error: "Error al agregar la familia" });
  }
});

// ✅ EDIT A LA TABLA FAMILIA
router.post("/edit-familia", async (req, res) => {
  const { codigo, nombreFamilia, representante, direccion, telefono } = req.body;

  if (!codigo || !nombreFamilia || !representante || !direccion || !telefono) {
      return res.status(400).json({ error: "Todos los campos son obligatorios" });
  }

  try {
    const [result] = await connection.query(
      "UPDATE familias SET codigo_familia = ?, nombre_familia = ?, representante = ?, direccion = ?, telefono = ? WHERE codigo_familia = ?",
      [codigo, nombreFamilia, representante, direccion, telefono, codigo]
  );

      res.status(201).json({ message: "Familia agregada correctamente", id: result.insertId });
  } catch (error) {
      console.error("Error al agregar familia:", error);
      res.status(500).json({ error: "Error al agregar la familia" });
  }
});

// ✅ DELETE A LA TABLA FAMILIA
router.post("/delete-familia", async (req, res) => {
  const { codigo, nombreFamilia, representante, direccion, telefono } = req.body;

  if (!codigo || !nombreFamilia || !representante || !direccion || !telefono) {
      return res.status(400).json({ error: "Todos los campos son obligatorios" });
  }

  try {
    const [result] = await connection.query(
      "DELETE FROM familias where codigo_familia = ?",
      [codigo]
  );

      res.status(201).json({ message: "Familia eliminada correctamente", id: result.insertId });
  } catch (error) {
      console.error("Error al agregar familia:", error);
      res.status(500).json({ error: "Error al agregar la familia" });
  }
});







// ✅ OBTENER DATOS DE LA TABLA PERSONA
router.get("/personas_t", async (req, res) => {
  try {
    const [rows] = await connection.query("SELECT * FROM personas");
    res.json(rows);
  } catch (error) {
    console.error("Error al obtener datos de personas:", error);
    res.status(500).json({ error: "Error al obtener datos de la base de datos" });
  }
});
// ✅ AGREGAR A LA TABLA PERSONA
router.post("/agregar-persona", async (req, res) => {
  const { codigo, nombres, apellidos, telefono, email, estado, propiedad } = req.body;

  if (!codigo || !nombres || !apellidos || !telefono || !propiedad) {
      return res.status(400).json({ error: "Todos los campos son obligatorios" });
  }

  try {
      const [result] = await connection.query(
          "INSERT INTO personas (codigo_familia, nombres, apellidos, telefono, email, estado, propiedad) VALUES (?, ?, ?, ?, ?, ?, ?)",
          [codigo, nombres, apellidos, telefono, email, estado, propiedad]
      );

      res.status(201).json({ message: "Persona agregada correctamente", id: result.insertId });
  } catch (error) {
      console.error("Error al agregar persona:", error);
      res.status(500).json({ error: "Error al agregar la persona" });
  }
});

// ✅ EDIT A LA TABLA PERSONA
router.post("/edit-persona", async (req, res) => {
  const { codigo, nombres, apellidos, telefono, email, estado, propiedad, id } = req.body;

  if (!codigo || !nombres || !apellidos || !telefono || !propiedad) {
      return res.status(400).json({ error: "Todos los campos son obligatorios" });
  }

  try {
    const [result] = await connection.query(
      "UPDATE personas SET codigo_familia = ?, nombres = ?, apellidos = ?, telefono = ?, email = ?, estado = ?, propiedad = ? WHERE id = ?",
      [codigo, nombres, apellidos, telefono, email, estado, propiedad, id]
  );

      res.status(201).json({ message: "Familia agregada correctamente", id: result.insertId });
  } catch (error) {
      console.error("Error al agregar familia:", error);
      res.status(500).json({ error: "Error al agregar la familia" });
  }
});

// ✅ DELETE A LA TABLA PERSONA
router.post("/delete-persona", async (req, res) => {
  const { codigo} = req.body;

  if (!codigo) {
      return res.status(400).json({ error: "Todos los campos son obligatorios" });
  }

  try {
    const [result] = await connection.query(
      "DELETE FROM personas where id = ?",
      [codigo]
  );

      res.status(201).json({ message: "Persona eliminada correctamente", id: result.insertId });
  } catch (error) {
      console.error("Error al agregar persona:", error);
      res.status(500).json({ error: "Error al agregar la persona" });
  }
});





//PARA CODIGOS QR
router.post("/validarqr", async (req, res) => {
  const { id_usuario, codigo_familia, hora_generacion, hora_vencimiento } = req.body;

  // Validación de los campos requeridos
  if (!id_usuario || !codigo_familia || !hora_generacion || !hora_vencimiento) {
    return res.status(400).json({ message: "Todos los datos del QR son requeridos." });
  }

  try {
    // Verificar si el QR es válido en la tabla 'qrs_generados'
    const [results] = await connection.query(
      `SELECT * FROM qrs_generados 
       WHERE id_usuario = ? AND codigo_familia = ? AND hora_generacion = ? AND hora_vencimiento >= ?`,
      [id_usuario, codigo_familia, hora_generacion, hora_vencimiento]
    );

    if (results.length === 0) {
      return res.status(404).json({ message: "QR no válido o expirado." });
    }

    // Si el QR es válido, insertar el visitante en la tabla 'visitantes'
    const [insertResult] = await connection.query(
      "INSERT INTO visitantes (id_usuario, codigo_familia, hora_entrada) VALUES (?, ?, NOW())",
      [id_usuario, codigo_familia]
    );

    res.status(200).json({ message: "Visitante registrado exitosamente." });
  } catch (error) {
    console.error("Error al procesar el QR:", error);
    res.status(500).json({ message: "Error interno del servidor." });
  }
});


module.exports = router;
