import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from langchain.schema.output_parser import StrOutputParser
import openai
load_dotenv(find_dotenv())

class ChatbotService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key

        self.vectorstore = DocArrayInMemorySearch.from_texts(
            [
                "Sofá Minimalista, 500 USD, Este sofá de dos plazas es la definición de minimalismo moderno. Sus líneas rectas y limpias crean una estética elegante y atemporal, mientras que sus cojines generosamente rellenos brindan comodidad inigualable. Perfecto para espacios pequeños o como complemento en salas de estar amplias, este sofá se adapta a cualquier decoración. Tapizado en tela de alta calidad disponible en una variedad de colores neutros para combinar con cualquier estilo. Estructura de madera maciza para mayor durabilidad y soporte. Patas de metal con acabado cromado que aportan un toque de sofisticación. Cojines desenfundables para facilitar la limpieza.",
                "Mesa de Centro Rústica, 150 USD, Esta mesa de centro rústica está hecha de madera recuperada, lo que le da un encanto único y auténtico. Su diseño robusto y resistente la convierte en una pieza duradera que complementará cualquier decoración de estilo rústico o industrial. Superficie de madera con acabado natural que muestra las marcas y vetas de la madera recuperada. Patas gruesas que brindan estabilidad y soporte. Amplio espacio de almacenamiento en la parte inferior para guardar libros, revistas o mantas. Hecho a mano por artesanos expertos, cada mesa es única.",
                "Silla de Comedor Vintage, 75 USD, Transporta tu comedor a otra época con esta silla vintage. Su diseño clásico con detalles tallados y su acabado envejecido le dan un encanto atemporal que nunca pasa de moda. Estructura de madera maciza para mayor durabilidad. Asiento y respaldo tapizados en tela de terciopelo suave y cómodo. Patas curvadas que aportan un toque elegante. Disponible en una variedad de colores para combinar con cualquier decoración.",
                "Lámpara de Pie Industrial, 120 USD, Esta lámpara de pie de estilo industrial aportará un toque de personalidad y funcionalidad a tu espacio. Su diseño de metal con acabado rústico y su pantalla ajustable te permiten dirigir la luz donde la necesites. Base de metal resistente que proporciona estabilidad. Pantalla de metal ajustable que permite dirigir la luz. Bombilla LED de bajo consumo incluida. Perfecta para salas de estar, dormitorios, oficinas o cualquier espacio que necesite iluminación adicional.",
                "Estantería de Pared Flotante, 90 USD, Esta estantería de pared flotante es la solución perfecta para almacenar libros, decoración y otros objetos pequeños. Su diseño minimalista y moderno la hace ideal para cualquier espacio. Fácil instalación con instrucciones claras y herrajes incluidos. Superficie de madera resistente que soporta hasta 10 kg de peso. Disponible en diferentes longitudes para adaptarse a tus necesidades de almacenamiento. Aporta un toque de sofisticación y organización a cualquier pared.",
                "Sofá Seccional de Cuero, 800 USD, Este sofá seccional de cuero negro es la pieza ideal para amueblar una sala de estar amplia y acogedora. Su diseño modular te permite configurarlo de diferentes maneras para adaptarse a tus necesidades de espacio. Tapizado en cuero negro de alta calidad que es duradero y fácil de limpiar. Cojines rellenos de espuma de alta densidad para mayor comodidad. Incluye una chaise longue incorporada para mayor relajación. Estructura de madera maciza para mayor durabilidad y soporte.",
                "Mesa de Comedor Expandible, 400 USD, Esta mesa de comedor expandible es perfecta para familias o grupos grandes. Su capacidad de expandirse de 6 a 8 comensales la hace ideal para cualquier ocasión. Superficie de madera maciza disponible en diferentes acabados. Patas extensibles que se pliegan fácilmente cuando no están en uso. Amplio espacio para acomodar a todos tus invitados. Diseño clásico que combina con cualquier decoración.",
                "Sillón Recliner Eléctrico, 300 USD, Este sillón reclinable eléctrico te brinda la máxima comodidad y relajación. Con su función reclinable eléctrica y soporte lumbar ajustable, puedes encontrar la posición perfecta para descansar. Tapizado en tela suave y transpirable disponible en una variedad de colores. Función reclinable eléctrica con control remoto para un fácil uso. Soporte lumbar ajustable.",
                "Escritorio de Oficina Moderno, 200 USD, Este escritorio de oficina moderno combina funcionalidad y estilo. Su superficie de vidrio templado y estructura de metal cromado ofrecen un espacio de trabajo amplio y resistente. Espacio de almacenamiento lateral con cajones para mantener tu área de trabajo ordenada. Diseño elegante que se adapta a cualquier oficina o estudio. Patas ajustables para mayor estabilidad en cualquier superficie.",
                "Lámpara de Techo Moderna, 180 USD, Esta lámpara de techo moderna es perfecta para iluminar cualquier espacio con estilo. Su diseño contemporáneo y luz LED integrada ofrecen una iluminación eficiente y de larga duración. Pantalla de vidrio esmerilado que proporciona una luz suave y difusa. Instalación sencilla con herrajes incluidos. Disponible en varios acabados para combinar con tu decoración.",
                "Sofá Cama Convertible, 600 USD, Este sofá cama convertible es la solución ideal para espacios pequeños. Durante el día, es un cómodo sofá, y por la noche se transforma en una cama doble. Tapizado en tela resistente y fácil de limpiar. Mecanismo de conversión simple y rápido. Cojines rellenos de espuma de alta densidad para mayor comodidad.",
                "Butaca Retro, 250 USD, Añade un toque de nostalgia a tu sala de estar con esta butaca retro. Su diseño de los años 60 y su tapizado en terciopelo la hacen una pieza única y acogedora. Estructura de madera maciza para mayor durabilidad. Cojines mullidos que ofrecen una gran comodidad. Disponible en varios colores vibrantes.",
                "Mesa Auxiliar Nórdica, 70 USD, Esta mesa auxiliar nórdica es perfecta para complementar cualquier espacio con su diseño sencillo y elegante. Superficie de madera clara con patas de madera maciza. Ligera y fácil de mover. Ideal para usar como mesa de noche o mesa auxiliar en el salón.",
                "Silla de Oficina Ergonómica, 150 USD, Esta silla de oficina ergonómica está diseñada para proporcionar el máximo confort durante largas horas de trabajo. Asiento y respaldo ajustables para adaptarse a tu postura. Tapizado en tela transpirable que mantiene fresco. Base giratoria con ruedas para mayor movilidad. Disponible en varios colores.",
                "Sofá Chesterfield, 700 USD, Este clásico sofá Chesterfield aporta un toque de elegancia a cualquier sala de estar. Tapizado en cuero marrón de alta calidad con capitoné. Cojines rellenos de espuma de alta densidad para mayor comodidad. Estructura de madera maciza para mayor durabilidad. Patas de madera con acabado oscuro.",
                "Lámpara de Mesa Escandinava, 50 USD, Esta lámpara de mesa escandinava es perfecta para añadir un toque de estilo y funcionalidad a cualquier espacio. Base de madera maciza con pantalla de tela blanca. Luz LED de bajo consumo incluida. Interruptor de encendido/apagado en el cable. Diseño compacto que se adapta a cualquier mesa o escritorio.",
                "Banco de Entrada Tapizado, 120 USD, Este banco de entrada tapizado es una solución elegante y práctica para tu recibidor. Cojín cómodo para sentarse mientras te pones los zapatos. Compartimento de almacenamiento debajo del asiento. Tapizado en tela resistente disponible en varios colores. Estructura de madera maciza para mayor durabilidad.",
                "Mesa de Noche Moderna, 100 USD, Esta mesa de noche moderna ofrece un espacio de almacenamiento funcional y un diseño elegante. Dos cajones amplios para guardar tus pertenencias. Superficie de madera con acabado liso y brillante. Patas de metal con acabado cromado. Fácil de montar con instrucciones incluidas.",
                "Sillón de Lectura, 280 USD, Este sillón de lectura es el lugar perfecto para relajarse con un buen libro. Asiento amplio y cómodo con cojines de espuma de alta densidad. Tapizado en tela suave y duradera. Estructura de madera maciza para mayor durabilidad. Disponible en varios colores para combinar con tu decoración.",
                "Mesa de TV con Almacenamiento, 300 USD, Esta mesa de TV con almacenamiento es ideal para mantener tu sala de estar ordenada y organizada. Amplio espacio para tu TV y dispositivos multimedia. Estantes y cajones para guardar libros, juegos y otros accesorios. Estructura de madera resistente con acabado elegante. Fácil de montar con instrucciones incluidas.",
                "Espejo de Pared Decorativo, 90 USD, Este espejo de pared decorativo añade un toque de elegancia a cualquier habitación. Marco decorativo disponible en varios estilos y acabados. Superficie de espejo de alta calidad que proporciona una imagen clara. Fácil de colgar con herrajes incluidos. Ideal para salas de estar, dormitorios o entradas.",
                "Alfombra de Lana Natural, 250 USD, Esta alfombra de lana natural añade calidez y comodidad a cualquier espacio. Hecha de lana 100% natural, suave y duradera. Disponible en varios tamaños y colores. Fácil de limpiar y mantener. Perfecta para salas de estar, dormitorios y oficinas.",
                "Mesa de Jardín Plegable, 180 USD, Esta mesa de jardín plegable es perfecta para disfrutar de tus espacios exteriores. Estructura de metal resistente con acabado resistente a la intemperie. Fácil de plegar y almacenar cuando no está en uso. Superficie amplia para comidas y reuniones al aire libre. Disponible en varios colores.",
                "Sofá Modular de Tela, 550 USD, Este sofá modular de tela ofrece flexibilidad y confort en cualquier sala de estar. Secciones móviles que permiten configurarlo de diferentes maneras. Tapizado en tela suave y lavable. Cojines rellenos de espuma de alta densidad para mayor comodidad. Estructura de madera maciza para mayor durabilidad.",
                "Lámpara de Piso Contemporánea, 130 USD, Esta lámpara de piso contemporánea añade un toque de estilo moderno a cualquier espacio. Base de metal con acabado elegante. Pantalla ajustable para dirigir la luz. Bombilla LED de bajo consumo incluida. Ideal para salas de estar, dormitorios o oficinas."
            ],
            embedding=OpenAIEmbeddings()
        )

        self.retriever = self.vectorstore.as_retriever()
        self.memory = []
        self.template = """Responda la pregunta basándose únicamente en el siguiente contexto:
        {context}

        Sos un asistente virtual vendedor de Muebles. Tu objetivo es atender al cliente con un trato cordial y ayudarlo a encontrar el mueble perfecto para sus necesidades. Brindá toda la información necesaria sobre nuestros productos y servicios.

        Question: {question}
        
        Contexto de la conversacion: {memoria}
        """

        self.prompt = ChatPromptTemplate.from_template(self.template)

        self.model = ChatOpenAI()
        self.output_parser = StrOutputParser()

        self.chain = RunnableMap({
            "context": lambda x: self.retriever.invoke(x["question"]),
            "question": lambda x: x["question"],
            "memoria": lambda x: "\n".join(self.memory)
        }) | self.prompt | self.model | self.output_parser

    def get_response(self, chat_id: str, question: str) -> str:
        response= self.chain.invoke({"question": question})    
        
        self.memory.append(f"Cliente: {question}")
        self.memory.append(f"Asistente: {response}")

        return response

