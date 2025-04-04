
using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;

public class FileManager
{

   public void InputFile(List<Figure> figures)
   {
        var settings = new JsonSerializerSettings
        {
            TypeNameHandling = TypeNameHandling.Auto,
            Formatting = Formatting.Indented
        };

        string json = JsonConvert.SerializeObject(figures, settings);
        File.WriteAllText("storage.json", json);                                                                                                                                                                                                                

   }

   
   public List<Figure> OutputFile() {

        string json = File.ReadAllText("storage.json");

        var settings = new JsonSerializerSettings
        {
            TypeNameHandling = TypeNameHandling.Auto
        };


        List<Figure>? figures = JsonConvert.DeserializeObject<List<Figure>>(json, settings);

        return figures;
    }

}
