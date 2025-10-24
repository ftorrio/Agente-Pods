# -*- coding: utf-8 -*-
"""
Interfaz Gráfica para el Sistema de Validación de PODs
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import sys

from main import PODValidationSystem
from utils import load_config


class PODValidatorGUI:
    """
    Interfaz gráfica principal para la validación de PODs
    """
    
    def __init__(self, root):
        """
        Inicializa la interfaz gráfica
        
        Args:
            root: Ventana raíz de Tkinter
        """
        self.root = root
        self.root.title("Sistema de Validación de PODs")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Variables
        self.input_directory = tk.StringVar()
        self.processing = False
        self.results = []
        self.system = None
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
        # Cargar directorio por defecto
        config = load_config()
        if config:
            default_dir = config['paths']['input_dir']
            if os.path.exists(default_dir):
                self.input_directory.set(default_dir)
    
    def setup_styles(self):
        """
        Configura los estilos de la interfaz
        """
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores
        self.color_ok = "#28a745"
        self.color_warning = "#ffc107"
        self.color_error = "#dc3545"
        self.color_info = "#17a2b8"
        self.color_bg = "#f8f9fa"
        self.color_fg = "#212529"
        
        # Estilos personalizados
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Status.TLabel", font=("Segoe UI", 10))
        style.configure("Stats.TLabel", font=("Segoe UI", 14, "bold"))
        
        # Estilo para el Treeview
        style.configure("Results.Treeview", rowheight=30, font=("Segoe UI", 9))
        style.configure("Results.Treeview.Heading", font=("Segoe UI", 10, "bold"))
    
    def create_widgets(self):
        """
        Crea todos los widgets de la interfaz
        """
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Configurar grid del frame principal
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # --- SECCIÓN 1: ENCABEZADO ---
        self.create_header(main_frame)
        
        # --- SECCIÓN 2: CONTROLES ---
        self.create_controls(main_frame)
        
        # --- SECCIÓN 3: ESTADÍSTICAS ---
        self.create_statistics(main_frame)
        
        # --- SECCIÓN 4: TABLA DE RESULTADOS ---
        self.create_results_table(main_frame)
        
        # --- SECCIÓN 5: CONSOLA/LOG ---
        self.create_log_console(main_frame)
        
        # --- SECCIÓN 6: BOTONES DE ACCIÓN ---
        self.create_action_buttons(main_frame)
    
    def create_header(self, parent):
        """
        Crea el encabezado de la aplicación
        """
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        title = ttk.Label(
            header_frame, 
            text="🔍 Sistema de Validación de PODs",
            style="Title.TLabel"
        )
        title.pack()
        
        subtitle = ttk.Label(
            header_frame,
            text="Proof of Delivery - Análisis Automático de Documentos",
            style="Status.TLabel"
        )
        subtitle.pack()
    
    def create_controls(self, parent):
        """
        Crea los controles de selección y procesamiento
        """
        control_frame = ttk.LabelFrame(parent, text="Control", padding="10")
        control_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Directorio de entrada
        dir_frame = ttk.Frame(control_frame)
        dir_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(dir_frame, text="Directorio:").pack(side="left", padx=(0, 5))
        
        dir_entry = ttk.Entry(dir_frame, textvariable=self.input_directory, width=60)
        dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(
            dir_frame, 
            text="📁 Explorar",
            command=self.browse_directory
        )
        browse_btn.pack(side="left")
        
        # Botones de acción principal
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill="x")
        
        self.process_btn = ttk.Button(
            button_frame,
            text="▶️ Procesar PODs",
            command=self.start_processing,
            style="Accent.TButton"
        )
        self.process_btn.pack(side="left", padx=(0, 5))
        
        self.stop_btn = ttk.Button(
            button_frame,
            text="⏹️ Detener",
            command=self.stop_processing,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=(0, 5))
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Limpiar",
            command=self.clear_results
        )
        self.clear_btn.pack(side="left")
    
    def create_statistics(self, parent):
        """
        Crea la sección de estadísticas
        """
        stats_frame = ttk.LabelFrame(parent, text="Estadísticas", padding="10")
        stats_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        # Contenedor de estadísticas
        stats_container = ttk.Frame(stats_frame)
        stats_container.pack(fill="x")
        
        # Total
        total_frame = ttk.Frame(stats_container)
        total_frame.pack(side="left", expand=True, fill="both")
        
        self.total_label = ttk.Label(total_frame, text="0", style="Stats.TLabel")
        self.total_label.pack()
        ttk.Label(total_frame, text="Total PODs").pack()
        
        # Válidos
        valid_frame = ttk.Frame(stats_container)
        valid_frame.pack(side="left", expand=True, fill="both")
        
        self.valid_label = ttk.Label(
            valid_frame, 
            text="0", 
            style="Stats.TLabel",
            foreground=self.color_ok
        )
        self.valid_label.pack()
        ttk.Label(valid_frame, text="✓ Válidos").pack()
        
        # Inválidos
        invalid_frame = ttk.Frame(stats_container)
        invalid_frame.pack(side="left", expand=True, fill="both")
        
        self.invalid_label = ttk.Label(
            invalid_frame, 
            text="0", 
            style="Stats.TLabel",
            foreground=self.color_error
        )
        self.invalid_label.pack()
        ttk.Label(invalid_frame, text="✗ Con Defectos").pack()
        
        # OK
        ok_frame = ttk.Frame(stats_container)
        ok_frame.pack(side="left", expand=True, fill="both")
        
        self.ok_label = ttk.Label(ok_frame, text="0", style="Stats.TLabel")
        self.ok_label.pack()
        ttk.Label(ok_frame, text="OK").pack()
        
        # Con Anotaciones
        annotations_frame = ttk.Frame(stats_container)
        annotations_frame.pack(side="left", expand=True, fill="both")
        
        self.annotations_label = ttk.Label(annotations_frame, text="0", style="Stats.TLabel")
        self.annotations_label.pack()
        ttk.Label(annotations_frame, text="Con Anotaciones").pack()
        
        # Sin Acuse
        no_ack_frame = ttk.Frame(stats_container)
        no_ack_frame.pack(side="left", expand=True, fill="both")
        
        self.no_ack_label = ttk.Label(no_ack_frame, text="0", style="Stats.TLabel")
        self.no_ack_label.pack()
        ttk.Label(no_ack_frame, text="Sin Acuse").pack()
        
        # Porcentaje
        percentage_frame = ttk.Frame(stats_container)
        percentage_frame.pack(side="left", expand=True, fill="both")
        
        self.percentage_label = ttk.Label(
            percentage_frame, 
            text="0%", 
            style="Stats.TLabel",
            foreground=self.color_info
        )
        self.percentage_label.pack()
        ttk.Label(percentage_frame, text="Tasa Validación").pack()
    
    def create_results_table(self, parent):
        """
        Crea la tabla de resultados
        """
        table_frame = ttk.LabelFrame(parent, text="Resultados Detallados", padding="10")
        table_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        
        parent.rowconfigure(3, weight=1)
        
        # Crear Treeview con scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        
        self.results_tree = ttk.Treeview(
            table_frame,
            columns=("archivo", "clasificacion", "valido", "confianza", "firmas", "sellos", "anotaciones", "problemas"),
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            style="Results.Treeview"
        )
        
        tree_scroll_y.config(command=self.results_tree.yview)
        tree_scroll_x.config(command=self.results_tree.xview)
        
        # Definir columnas
        self.results_tree.heading("archivo", text="Archivo")
        self.results_tree.heading("clasificacion", text="Clasificación")
        self.results_tree.heading("valido", text="Estado")
        self.results_tree.heading("confianza", text="Confianza")
        self.results_tree.heading("firmas", text="Firmas")
        self.results_tree.heading("sellos", text="Sellos")
        self.results_tree.heading("anotaciones", text="Anotaciones")
        self.results_tree.heading("problemas", text="Problemas/Detalles")
        
        # Configurar anchos
        self.results_tree.column("archivo", width=200, minwidth=150)
        self.results_tree.column("clasificacion", width=150, minwidth=100)
        self.results_tree.column("valido", width=80, minwidth=80)
        self.results_tree.column("confianza", width=80, minwidth=80)
        self.results_tree.column("firmas", width=60, minwidth=50)
        self.results_tree.column("sellos", width=60, minwidth=50)
        self.results_tree.column("anotaciones", width=100, minwidth=80)
        self.results_tree.column("problemas", width=300, minwidth=200)
        
        # Layout
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Bind double-click para ver detalles
        self.results_tree.bind("<Double-1>", self.show_details)
        
        # Tags para colores
        self.results_tree.tag_configure("valid", background="#d4edda")
        self.results_tree.tag_configure("invalid", background="#f8d7da")
        self.results_tree.tag_configure("warning", background="#fff3cd")
    
    def create_log_console(self, parent):
        """
        Crea la consola de log
        """
        log_frame = ttk.LabelFrame(parent, text="Log de Procesamiento", padding="10")
        log_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        
        self.log_text = ScrolledText(log_frame, height=8, wrap=tk.WORD)
        self.log_text.pack(fill="both", expand=True)
        
        # Configurar tags para colores
        self.log_text.tag_configure("INFO", foreground="black")
        self.log_text.tag_configure("SUCCESS", foreground=self.color_ok)
        self.log_text.tag_configure("WARNING", foreground=self.color_warning)
        self.log_text.tag_configure("ERROR", foreground=self.color_error)
    
    def create_action_buttons(self, parent):
        """
        Crea los botones de acción inferior
        """
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=5, column=0, sticky="ew")
        
        ttk.Button(
            action_frame,
            text="📊 Abrir Reportes",
            command=self.open_reports_folder
        ).pack(side="left", padx=(0, 5))
        
        ttk.Button(
            action_frame,
            text="🖼️ Ver Imágenes Anotadas",
            command=self.open_images_folder
        ).pack(side="left", padx=(0, 5))
        
        ttk.Button(
            action_frame,
            text="📋 Exportar Excel",
            command=self.export_excel
        ).pack(side="left", padx=(0, 5))
        
        ttk.Button(
            action_frame,
            text="❓ Ayuda",
            command=self.show_help
        ).pack(side="right")
    
    # --- MÉTODOS DE FUNCIONALIDAD ---
    
    def browse_directory(self):
        """
        Abre diálogo para seleccionar directorio
        """
        directory = filedialog.askdirectory(
            title="Seleccionar directorio con PODs",
            initialdir=self.input_directory.get() or "."
        )
        if directory:
            self.input_directory.set(directory)
    
    def start_processing(self):
        """
        Inicia el procesamiento de PODs en un hilo separado
        """
        input_dir = self.input_directory.get()
        
        if not input_dir or not os.path.exists(input_dir):
            messagebox.showerror(
                "Error",
                "Por favor selecciona un directorio válido"
            )
            return
        
        # Verificar que hay archivos
        from utils import get_files_from_directory
        config = load_config()
        files = get_files_from_directory(input_dir, config['supported_formats'])
        
        if not files:
            messagebox.showwarning(
                "Advertencia",
                f"No se encontraron archivos POD en:\n{input_dir}\n\n"
                "Formatos soportados: PDF, GIF, PNG, JPG, TIFF, BMP"
            )
            return
        
        # Limpiar resultados anteriores
        self.clear_results()
        
        # Iniciar procesamiento
        self.processing = True
        self.process_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        
        self.log("INFO", f"Iniciando procesamiento de {len(files)} archivo(s)...")
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self.process_documents, args=(input_dir,))
        thread.daemon = True
        thread.start()
    
    def process_documents(self, input_dir):
        """
        Procesa los documentos (ejecutado en hilo separado)
        """
        try:
            # Inicializar sistema
            self.system = PODValidationSystem()
            
            # Obtener archivos
            from utils import get_files_from_directory
            files = get_files_from_directory(input_dir, self.system.config['supported_formats'])
            
            for idx, file_path in enumerate(files, 1):
                if not self.processing:
                    self.log("WARNING", "Procesamiento detenido por el usuario")
                    break
                
                self.log("INFO", f"[{idx}/{len(files)}] Procesando: {os.path.basename(file_path)}")
                
                try:
                    result = self.system.process_single_file(file_path, save_annotated=True)
                    if result:
                        self.results.append(result)
                        self.root.after(0, self.add_result_to_table, result)
                        self.root.after(0, self.update_statistics)
                        
                        # Log del resultado
                        status = "✓" if result['is_valid'] else "✗"
                        tag = "SUCCESS" if result['is_valid'] else "ERROR"
                        self.log(
                            tag, 
                            f"{status} {os.path.basename(file_path)}: {result['classification']}"
                        )
                except Exception as e:
                    self.log("ERROR", f"Error procesando {os.path.basename(file_path)}: {str(e)}")
            
            # Finalizar
            if self.processing:
                self.log("SUCCESS", f"\n✅ Procesamiento completado: {len(self.results)} documento(s)")
                self.root.after(0, messagebox.showinfo, "Completado", 
                               f"Se procesaron {len(self.results)} documento(s)\n\n"
                               f"Válidos: {sum(1 for r in self.results if r['is_valid'])}\n"
                               f"Con defectos: {sum(1 for r in self.results if not r['is_valid'])}")
        
        except Exception as e:
            self.log("ERROR", f"Error general: {str(e)}")
            self.root.after(0, messagebox.showerror, "Error", f"Error durante el procesamiento:\n{str(e)}")
        
        finally:
            self.processing = False
            self.root.after(0, self.process_btn.config, {"state": "normal"})
            self.root.after(0, self.stop_btn.config, {"state": "disabled"})
    
    def stop_processing(self):
        """
        Detiene el procesamiento
        """
        self.processing = False
        self.log("WARNING", "Deteniendo procesamiento...")
    
    def add_result_to_table(self, result: Dict[str, Any]):
        """
        Agrega un resultado a la tabla
        """
        filename = os.path.basename(result['source_file'])
        classification = result['classification']
        is_valid = "✓ Válido" if result['is_valid'] else "✗ Defecto"
        confidence = f"{result['confidence']:.0%}"
        
        # Contar detecciones
        num_signatures = len(result['details'].get('signatures', []))
        num_stamps = len(result['details'].get('stamps', []))
        
        annotations = result['details'].get('annotations', {})
        annotation_text = "No"
        if annotations.get('has_annotations'):
            sentiment = annotations.get('sentiment', 'neutral')
            sentiment_emoji = {"positive": "✓", "negative": "✗", "neutral": "○"}
            annotation_text = f"{sentiment_emoji.get(sentiment, '○')} {sentiment}"
        
        # Problemas (primeros 2)
        problems = result.get('issues', [])
        problems_text = " | ".join(problems[:2]) if problems else "Ninguno"
        if len(problems) > 2:
            problems_text += f" (+{len(problems)-2} más)"
        
        # Tag según validez
        tag = "valid" if result['is_valid'] else "invalid"
        if classification == "CON ANOTACIONES":
            tag = "warning"
        
        # Insertar en la tabla
        self.results_tree.insert(
            "",
            "end",
            values=(
                filename,
                classification,
                is_valid,
                confidence,
                num_signatures,
                num_stamps,
                annotation_text,
                problems_text
            ),
            tags=(tag,)
        )
    
    def update_statistics(self):
        """
        Actualiza las estadísticas mostradas
        """
        if not self.results:
            return
        
        total = len(self.results)
        valid = sum(1 for r in self.results if r['is_valid'])
        invalid = total - valid
        
        # Por clasificación
        ok_count = sum(1 for r in self.results if r['classification_code'] == 'OK')
        annotations_count = sum(1 for r in self.results if r['classification_code'] == 'CON_ANOTACIONES')
        no_ack_count = sum(1 for r in self.results if r['classification_code'] == 'SIN_ACUSE')
        
        # Porcentaje
        percentage = (valid / total * 100) if total > 0 else 0
        
        # Actualizar labels
        self.total_label.config(text=str(total))
        self.valid_label.config(text=str(valid))
        self.invalid_label.config(text=str(invalid))
        self.ok_label.config(text=str(ok_count))
        self.annotations_label.config(text=str(annotations_count))
        self.no_ack_label.config(text=str(no_ack_count))
        self.percentage_label.config(text=f"{percentage:.1f}%")
    
    def clear_results(self):
        """
        Limpia los resultados
        """
        self.results = []
        
        # Limpiar tabla
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Limpiar estadísticas
        self.total_label.config(text="0")
        self.valid_label.config(text="0")
        self.invalid_label.config(text="0")
        self.ok_label.config(text="0")
        self.annotations_label.config(text="0")
        self.no_ack_label.config(text="0")
        self.percentage_label.config(text="0%")
        
        # Limpiar log
        self.log_text.delete(1.0, tk.END)
        
        self.log("INFO", "Resultados limpiados")
    
    def show_details(self, event):
        """
        Muestra detalles de un resultado al hacer doble clic
        """
        selection = self.results_tree.selection()
        if not selection:
            return
        
        item = self.results_tree.item(selection[0])
        filename = item['values'][0]
        
        # Buscar resultado
        result = next((r for r in self.results if os.path.basename(r['source_file']) == filename), None)
        
        if not result:
            return
        
        # Crear ventana de detalles
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Detalles: {filename}")
        details_window.geometry("700x600")
        
        # Frame principal con scroll
        canvas = tk.Canvas(details_window)
        scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenido
        padding = {"padx": 20, "pady": 5}
        
        ttk.Label(scrollable_frame, text=f"📄 {filename}", style="Subtitle.TLabel").pack(**padding, anchor="w")
        
        ttk.Separator(scrollable_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Clasificación
        ttk.Label(scrollable_frame, text="Clasificación:", font=("Segoe UI", 10, "bold")).pack(**padding, anchor="w")
        ttk.Label(scrollable_frame, text=f"  {result['classification']}").pack(**padding, anchor="w")
        
        valid_text = "✓ Válido" if result['is_valid'] else "✗ Con Defectos"
        valid_color = self.color_ok if result['is_valid'] else self.color_error
        valid_label = ttk.Label(scrollable_frame, text=f"  {valid_text}", foreground=valid_color)
        valid_label.pack(**padding, anchor="w")
        
        ttk.Label(scrollable_frame, text=f"  Confianza: {result['confidence']:.1%}").pack(**padding, anchor="w")
        
        # Firmas
        ttk.Label(scrollable_frame, text="\nFirmas:", font=("Segoe UI", 10, "bold")).pack(**padding, anchor="w")
        signatures = result['details'].get('signatures', [])
        if signatures:
            for sig in signatures:
                ttk.Label(scrollable_frame, text=f"  • Región: {sig['region']}, Confianza: {sig['confidence']:.2f}").pack(**padding, anchor="w")
        else:
            ttk.Label(scrollable_frame, text="  No se detectaron firmas").pack(**padding, anchor="w")
        
        # Sellos
        ttk.Label(scrollable_frame, text="\nSellos:", font=("Segoe UI", 10, "bold")).pack(**padding, anchor="w")
        stamps = result['details'].get('stamps', [])
        if stamps:
            for stamp in stamps:
                valid_stamp = "✓ Válido" if stamp['is_valid'] else "✗ Inválido"
                ttk.Label(scrollable_frame, text=f"  • {stamp['type']}: {valid_stamp}").pack(**padding, anchor="w")
        else:
            ttk.Label(scrollable_frame, text="  No se detectaron sellos").pack(**padding, anchor="w")
        
        # Anotaciones
        ttk.Label(scrollable_frame, text="\nAnotaciones:", font=("Segoe UI", 10, "bold")).pack(**padding, anchor="w")
        annotations = result['details'].get('annotations', {})
        if annotations.get('has_annotations'):
            ttk.Label(scrollable_frame, text=f"  Cantidad: {annotations['annotation_count']}").pack(**padding, anchor="w")
            ttk.Label(scrollable_frame, text=f"  Sentimiento: {annotations['sentiment']}").pack(**padding, anchor="w")
            if annotations.get('text_content'):
                ttk.Label(scrollable_frame, text="  Texto extraído:").pack(**padding, anchor="w")
                for text in annotations['text_content'][:3]:
                    ttk.Label(scrollable_frame, text=f"    - {text[:60]}...").pack(**padding, anchor="w")
        else:
            ttk.Label(scrollable_frame, text="  No se detectaron anotaciones").pack(**padding, anchor="w")
        
        # Legibilidad
        ttk.Label(scrollable_frame, text="\nLegibilidad:", font=("Segoe UI", 10, "bold")).pack(**padding, anchor="w")
        legibility = result['details'].get('legibility', {})
        ttk.Label(scrollable_frame, text=f"  Calidad del texto: {legibility.get('text_quality', 0):.2f}").pack(**padding, anchor="w")
        ttk.Label(scrollable_frame, text=f"  Confianza OCR: {legibility.get('ocr_confidence', 0):.1f}").pack(**padding, anchor="w")
        ttk.Label(scrollable_frame, text=f"  Campos detectados: {', '.join(legibility.get('fields_detected', []))}").pack(**padding, anchor="w")
        
        # Problemas
        ttk.Label(scrollable_frame, text="\nProblemas:", font=("Segoe UI", 10, "bold")).pack(**padding, anchor="w")
        for issue in result.get('issues', []):
            ttk.Label(scrollable_frame, text=f"  • {issue}").pack(**padding, anchor="w")
        
        # Recomendaciones
        if result.get('recommendations'):
            ttk.Label(scrollable_frame, text="\nRecomendaciones:", font=("Segoe UI", 10, "bold")).pack(**padding, anchor="w")
            for rec in result['recommendations']:
                ttk.Label(scrollable_frame, text=f"  → {rec}").pack(**padding, anchor="w")
        
        # Botón para ver imagen anotada
        if result.get('annotated_image_path'):
            def open_image():
                import subprocess
                subprocess.Popen(['explorer', result['annotated_image_path']])
            
            ttk.Button(
                scrollable_frame,
                text="🖼️ Ver Imagen Anotada",
                command=open_image
            ).pack(pady=20)
        
        # Layout
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def log(self, level: str, message: str):
        """
        Agrega mensaje al log
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, formatted_message, level)
        self.log_text.see(tk.END)
    
    def open_reports_folder(self):
        """
        Abre la carpeta de reportes
        """
        config = load_config()
        reports_dir = os.path.join(config['paths']['output_dir'], 'reportes')
        
        if os.path.exists(reports_dir):
            os.startfile(reports_dir)
        else:
            messagebox.showinfo("Info", "Aún no se han generado reportes")
    
    def open_images_folder(self):
        """
        Abre la carpeta de imágenes anotadas
        """
        config = load_config()
        images_dir = os.path.join(config['paths']['output_dir'], 'imagenes_anotadas')
        
        if os.path.exists(images_dir):
            os.startfile(images_dir)
        else:
            messagebox.showinfo("Info", "Aún no se han generado imágenes anotadas")
    
    def export_excel(self):
        """
        Exporta resultados a Excel
        """
        if not self.results:
            messagebox.showinfo("Info", "No hay resultados para exportar")
            return
        
        # Generar reportes usando el sistema
        if self.system:
            self.system._generate_reports(self.results)
            messagebox.showinfo("Éxito", "Reporte Excel generado en la carpeta de resultados")
            self.open_reports_folder()
    
    def show_help(self):
        """
        Muestra ayuda
        """
        help_text = """
SISTEMA DE VALIDACIÓN DE PODs

Clasificaciones:
• ✅ OK: Documento válido con firma/sello del cliente
• 📝 CON ANOTACIONES: Tiene comentarios manuscritos
• ⚠️ SIN ACUSE: Sin evidencia de recepción
• ❌ POCO LEGIBLE: Campos no distinguibles
• ❌ INCORRECTO: Documento cortado

Uso:
1. Selecciona el directorio con los PODs
2. Haz clic en "Procesar PODs"
3. Revisa los resultados en la tabla
4. Doble clic en un resultado para ver detalles

Formatos soportados:
PDF, GIF, PNG, JPG, TIFF, BMP

Para más información consulta:
- README.md
- GUIA_USO.md
        """
        
        messagebox.showinfo("Ayuda", help_text)


def main():
    """
    Función principal para ejecutar la GUI
    """
    root = tk.Tk()
    app = PODValidatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

