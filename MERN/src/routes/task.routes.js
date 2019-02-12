const express = require('express');
const Task =  require('../models/task');
const router = express.Router();

//Datos almacenados
router.get('/', async (req, res) =>{
   const task = await Task.find();
   console.log(task);
   res.json(task);
});
 router.get('/:id', async(req, res) =>{
    const task = await Task.findById(req.params.id);
    res.json(task);
 });
//registro a la base de datos
router.post('/', async(req, res) =>{
    const { name, email } = req.body;
    const task = new Task({name, email});
    console.log(task);
    await task.save();
    res.json({status: 'Task Saved'});
});

//Consulta a la base de datos para actualizar
router.put('/:id',async(req, res)=>{
    const {name, email} = req.body;
    const newTask = {name, email};
    await Task.findByIdAndUpdate(req.params.id, newTask);
    res.json({status: 'Task Updated'});
});
//Eliminar
router.delete('/:id', async(req, res)=>{
    await Task.findByIdAndRemove(req.params.id);
    res.json({status:'Task Deleted'});
});
module.exports = router;