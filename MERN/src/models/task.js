const mongoose = require('mongoose');
const {Schema} = mongoose;

const TaskSchema = new Schema({

    name: { type: String},
    email: { type: String}

});

module.exports= mongoose.model('Task', TaskSchema);