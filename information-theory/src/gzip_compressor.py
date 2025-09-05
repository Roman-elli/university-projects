import sys
import os
import numpy as np
from huffmantree import HuffmanTree
from config import *


class GZIPHeader:
	ID1 = ID2 = CM = FLG = XFL = OS = 0
	MTIME = []
	lenMTIME = 4
	mTime = 0

	# bits 0, 1, 2, 3 and 4, respectively (remaining 3 bits: reserved)
	FLG_FTEXT = FLG_FHCRC = FLG_FEXTRA = FLG_FNAME = FLG_FCOMMENT = 0

	# FLG_FTEXT --> ignored (usually 0)
	# if FLG_FEXTRA == 1
	XLEN, extraField = [], []
	lenXLEN = 2

	# if FLG_FNAME == 1
	fName = ''  # ends when a byte with value 0 is read

	# if FLG_FCOMMENT == 1
	fComment = ''   # ends when a byte with value 0 is read

	# if FLG_HCRC == 1
	HCRC = []



	def read(self, f):
		# ID 1 and 2: fixed values
		self.ID1 = f.read(1)[0]
		if self.ID1 != 0x1f: return -1 # error in the header

		self.ID2 = f.read(1)[0]
		if self.ID2 != 0x8b: return -1 # error in the header

		# CM - Compression Method: must be the value 8 for deflate
		self.CM = f.read(1)[0]
		if self.CM != 0x08: return -1 # error in the header

		# Flags
		self.FLG = f.read(1)[0]

		# MTIME
		self.MTIME = [0]*self.lenMTIME
		self.mTime = 0
		for i in range(self.lenMTIME):
			self.MTIME[i] = f.read(1)[0]
			self.mTime += self.MTIME[i] << (8 * i)

		# XFL (not processed...)
		self.XFL = f.read(1)[0]

		# OS (not processed...)
		self.OS = f.read(1)[0]

		# --- Check Flags
		self.FLG_FTEXT = self.FLG & 0x01
		self.FLG_FHCRC = (self.FLG & 0x02) >> 1
		self.FLG_FEXTRA = (self.FLG & 0x04) >> 2
		self.FLG_FNAME = (self.FLG & 0x08) >> 3
		self.FLG_FCOMMENT = (self.FLG & 0x10) >> 4

		# FLG_EXTRA
		if self.FLG_FEXTRA == 1:
			# read 2 bytes XLEN + XLEN bytes de extra field
			# 1st byte: LSB, 2nd: MSB
			self.XLEN = [0]*self.lenXLEN
			self.XLEN[0] = f.read(1)[0]
			self.XLEN[1] = f.read(1)[0]
			self.xlen = self.XLEN[1] << 8 + self.XLEN[0]

			# read extraField and ignore its values
			self.extraField = f.read(self.xlen)

		def read_str_until_0(f):
			s = ''
			while True:
				c = f.read(1)[0]
				if c == 0:
					return s
				s += chr(c)

		# FLG_FNAME
		if self.FLG_FNAME == 1:
			self.fName = read_str_until_0(f)

		# FLG_FCOMMENT
		if self.FLG_FCOMMENT == 1:
			self.fComment = read_str_until_0(f)

		# FLG_FHCRC (not processed...)
		if self.FLG_FHCRC == 1:
			self.HCRC = f.read(2)

		return 0

class GZIP:
	gzh = None
	gzFile = ''
	fileSize = origFileSize = -1
	numBlocks = 0
	f = None


	bits_buffer = 0
	available_bits = 0

	def __init__(self, filename):
		self.gzFile = filename
		self.f = open(filename, 'rb')
		self.f.seek(0,2)
		self.fileSize = self.f.tell()
		self.f.seek(0)

	def decompress(self):
		numBlocks = 0

		# get original file size: size of file before compression
		origFileSize = self.getOrigFileSize()
		print(origFileSize)

		# read GZIP header
		error = self.getHeader()
		if error != 0:
			print('Formato invalido!')
			return

		# show filename read from GZIP header
		print(self.gzh.fName)

		# MAIN LOOP - decode block by block
		BFINAL = 0
		while not BFINAL == 1:
			BFINAL = self.readBits(1)
			BTYPE = self.readBits(2)

			if BTYPE != 2:
				print('Error: Block %d not coded with Huffman Dynamic coding' % (numBlocks+1))
				return


			# Função que retorna os valores de HLIT, HDIST e HCLEN de acordo com a estrutura de cada bloco
			def tamanho_bloco():
				HLIT = self.readBits(5) + 257
				HDIST = self.readBits(5) + 1
				HCLEN = self.readBits(4) + 4
				return HLIT, HDIST, HCLEN
			
			# Função que busca armazenar os comprimentos dos codigos tendo como base HClen obtido anteriormente
			def array_bloco(HCLEN):
				ordem = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]
				resultado = [0] * len(ordem)
				for i in range(HCLEN):
					resultado[ordem[i]] = self.readBits(3)
				return resultado
			
			# Função que faz o histograma do array e retorna um array com 2 colunas (coluna 0 == simbolos e coluna 1 == ocorrencias), esta função leva em consideracao a 
			# ocorrência de todos os valores desde 0 até o maior simbolo.
			def histograma(array):
				valores, ocorrencias = np.unique(array, return_counts=True)
				histograma_simbolos = np.zeros((np.max(valores) + 1, 2), dtype=int)
				histograma_simbolos[:, 0] = np.arange(np.max(valores) + 1)
				histograma_simbolos[valores, 1] = ocorrencias
				return histograma_simbolos
			
			# A partir do histograma feito anteriormente, a função converte os codigos obtidos anteriormente em codigos de Huffman do "alfabeto de comprientos de códigos"
			def converte(array_resultado):
				ocorrencias = histograma(array_resultado)
				codigo = 0
				ocorrencias[0,1] = 0
				proximo_codigo = np.zeros(len(ocorrencias), dtype= int)
				for j in range (1, len(ocorrencias)):
					codigo = (codigo + ocorrencias[j - 1, 1]) << 1
					proximo_codigo[j] = codigo
					
				codigos = np.zeros(len(array_resultado), dtype= int)
			
				for j in range(len(array_resultado)):
					comprimento = array_resultado[j]
					if (comprimento != 0):
						codigos[j] = proximo_codigo[comprimento]
						proximo_codigo[comprimento] += 1
				return codigos
			
			# A partir do array na função array_bloco e o codigo gerado pela função converte, esta função gera uma arvore de huffman a qual é armazenado todos os dados obtidos
			# levando em conta os códigos que precisam da leitura de alguns bits extra.
			def constroi_arvore(array_resultado, codigo):
				arvore = HuffmanTree()
				for i in range (len(codigo)):
					if(array_resultado[i] != 0):
						string = bin(codigo[i])[2:]
						if(len(string) < array_resultado[i]):
							acrescenta = '0' * (array_resultado[i] - len(string))
							string = acrescenta + string
						arvore.addNode(string, i, False)
				return arvore
			
			# A partir da arvore obtida anteriormente e os comprimentos / distancias e códigos obtidos nas funçoes anteriores, esta função busca armazenar num array os 
			# literais/comprimentos, codificados nas últimas funções.
			def comp(HLIT, arvore):
				array = []
				while (len(array) < HLIT):
					arvore.resetCurNode()
					position = -2
					while position == -2:
						bit = self.readBits(1)
						position = arvore.nextNode(str(bit))
						if(position >= 0):
							break
						if(position == -1):
							print("erro")
							break
					if 0 <= position < 16:
						array.append(position)
					elif position == 16:
						bit = self.readBits(2)
						for i in range(3 + bit):
							array.append(array[-1])
					elif position == 17:
						bit = self.readBits(3)
						for i in range(3 + bit):
							array.append(0)
					elif(position == 18):
						bit = self.readBits(7)
						for i in range(11 + bit):
							array.append(0)
				return array
			
			# Função executada junto a função descompacta que adiciona ao array de dados os bits extra relacionados a distancia recuada e o comprimento que foram, ambos,
			# calculados na função descompacta.
			def descomprime(dados, comp, dist):
				x = len(dados) - dist
				if(x >= 0):
					for i in range(comp):
						dados.append(dados[x])
						x += 1
				else: 
					print("Erro no calculo de comprimento")
				return

			# Função que permite fazer a descompactacao dos dados comprimidos do bloco (data bytes) tendo como base os dicionários LZ77, sendo todos os casos de bits extra
			# devidamente acertados, tendo em conta o calculo do comprimento e da distancia. Tal função consiste em um ciclo while que apenas termina quando o fim do bloco é
			# alcançado, onde, durante sua execução consiste em uma leitura de duas arvores ao mesmo tempo, sendo a primeira arvore a ser lida, a arvore HLITtree e a segunda,
			# lida apenas case a variável pos seja superior a 256, sendo assim, nestes casos, feitos os devidos calculos do comprimento e da distancia em cada situação.
			def descompacta(dados_descompactados, HLITtree, HDISTtree):
				finaldobloco = True
	
				while(finaldobloco):
					HLITtree.resetCurNode()
					HDISTtree.resetCurNode()
					pos = -2

					while(pos == -2):
						bit= self.readBits(1)
						pos = HLITtree.nextNode(str(bit))
	
					if (pos == -1): 
						raise ValueError("Erro na árvore HLITtree")
					elif(pos < 256): 
						dados_descompactados.append(pos)
					elif(pos == 256): 
						finaldobloco = False
					elif(257 <= pos <= 285):
						if(257 <= pos <= 264 or pos == 285):
							if(pos == 285): 
								comp = 258
							else: 
								comp = pos - 254
						elif(265 <= pos <= 268):
							read = self.readBits(1)
							comp = pos - 254 + read + (pos - 265)
						elif(269 <= pos <= 272):
							read = self.readBits(2)
							comp = pos - 250 + read + (pos - 269) * 3 
						elif(273 <= pos <= 276):
							read = self.readBits(3)
							comp = pos - 238 + read + (pos - 273) * 7
						elif(277 <= pos <= 280):
							read = self.readBits(4)
							comp = pos - 210 + read + (pos - 277) * 15
						elif(281 <= pos <= 284):
							read = self.readBits(5)
							comp = pos - 150 + read + (pos - 281) * 31	
						else:
							raise ValueError("Erro ao ler o comprimento")
							finaldobloco = False
					
						posDist = -2

						while(posDist == -2):
							distBit = self.readBits(1)
							posDist = HDISTtree.nextNode(str(distBit))
							
							if (posDist == -1):
								raise ValueError("Erro na árvore HDISTtree")
								finaldobloco = False
								break
							elif(0 <= posDist <= 3): 
								dist = posDist + 1
							elif(4 <= posDist <= 5):
								readDist = self.readBits(1)
								dist = posDist + 1 + readDist + (posDist - 4)
							elif(6 <= posDist <= 7):
								readDist = self.readBits(2)
								dist = posDist + 3 + readDist + 3 * (posDist - 6)
							elif(8 <= posDist <= 9):
								readDist = self.readBits(3)
								dist = posDist + 9 + readDist + 7 * (posDist - 8)
							elif(10 <= posDist <= 11):
								readDist = self.readBits(4)
								dist = posDist + 23 + readDist + 15 * (posDist - 10)
							elif(12 <= posDist <= 13):
								readDist = self.readBits(5)
								dist = posDist + 53 + readDist + 31 * (posDist - 12)
							elif(14 <= posDist <= 15):
								readDist = self.readBits(6)
								dist = posDist + 115 + readDist + 63 * (posDist - 14)
							elif(16 <= posDist <= 17):
								readDist = self.readBits(7)
								dist = posDist + 241 + readDist + 127 * (posDist - 16)
							elif(18 <= posDist <= 19):
								readDist = self.readBits(8)
								dist = posDist + 495 + readDist + 255 * (posDist - 18)
							elif(20 <= posDist <= 21):
								readDist = self.readBits(9)
								dist = posDist + 1005 + readDist + 511 * (posDist - 20)
							elif(22 <= posDist <= 23):
								readDist = self.readBits(10)
								dist = posDist + 2027 + readDist + 1023 * (posDist - 22)
							elif(24 <= posDist <= 25):
								readDist = self.readBits(11)
								dist = posDist + 4073 + readDist + 2047 * (posDist - 24)
							elif(26 <= posDist <= 27):
								readDist = self.readBits(12)
								dist = posDist + 8167 + readDist + 4095 * (posDist - 26)
							elif(28 <= posDist <= 29):
								readDist = self.readBits(13)
								dist = posDist + 16357 + readDist + 8191 * (posDist - 28)	
						descomprime(dados_descompactados, comp, dist)
				return dados_descompactados
			
			# Função utilizada no final da execução da descompactação para que seja feita a tratação dos dados para que sejam inseridos no ficheiro.
			def writeFicheiro(dados):
				nomeFile = "../data/" + self.gzh.fName
				os.makedirs(os.path.dirname(nomeFile), exist_ok=True)
				file = open(nomeFile , 'wb')
				dados_byte = bytearray(dados)
				file.write(dados_byte)
				file.close()
		
			#-----------------------------# Questão 1 #-----------------------------#
			HLIT, HDIST, HCLEN = tamanho_bloco()

			#-----------------------------# Questão 2 #-----------------------------#
			array_resultado = array_bloco(HCLEN)

			#-----------------------------# Questão 3 #-----------------------------#
			codigo = converte(array_resultado)
			
			#-----------------------------# Questão 4 #-----------------------------#
			arvore = constroi_arvore(array_resultado, codigo)
			array_HLIT = comp(HLIT, arvore)

			#-----------------------------# Questão 5 #-----------------------------#
			array_HDIST = comp(HDIST, arvore)

			#-----------------------------# Questão 6 #-----------------------------#
			array_HLITconverte = converte(array_HLIT)
			array_HDISTconverte = converte(array_HDIST)

			#-----------------------------# Questão 7 #-----------------------------#
			HLITtree = constroi_arvore(array_HLIT, array_HLITconverte)
			HDISTtree = constroi_arvore(array_HDIST, array_HDISTconverte)
	
			if(numBlocks == 0): dados_descompactados = []
			dados_descompactados = descompacta(dados_descompactados, HLITtree, HDISTtree)

			#-----------------------------# Questão 8 #-----------------------------#
			if(BFINAL == 1): writeFicheiro(dados_descompactados)

			numBlocks += 1																									
		self.f.close()
		print("End: %d block(s) analyzed." % numBlocks)

	def getOrigFileSize(self):

		# saves current position of file pointer
		fp = self.f.tell()

		# jumps to end-4 position
		self.f.seek(self.fileSize-4)

		# reads the last 4 bytes (LITTLE ENDIAN)
		sz = 0
		for i in range(4):
			sz += self.f.read(1)[0] << (8*i)

		# restores file pointer to its original position
		self.f.seek(fp)

		return sz

	def getHeader(self):
		self.gzh = GZIPHeader()
		header_error = self.gzh.read(self.f)
		return header_error

	def readBits(self, n, keep=False):
		while n > self.available_bits:
			self.bits_buffer = self.f.read(1)[0] << self.available_bits | self.bits_buffer
			self.available_bits += 8

		mask = (2**n)-1
		value = self.bits_buffer & mask

		if not keep:
			self.bits_buffer >>= n
			self.available_bits -= n

		return value

def GZIPmenu():
    print("*** Welcome to gzip Decompressor!! ***\n")

    while True:
        print("(1) Image\n(2) Sound\n(3) Text\n(0) Exit")
        try:
            x = int(input("Write the number of the option of the file that you want to decompress: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if x == 0:
            print("\n\n*** Thank you for using GZIP Decompress!!! ***")
            return None

        if x == 1:
            folderPath = IMAGE_TEST_PATH
        elif x == 2:
            folderPath = SOUNDS_TEST_PATH
        elif x == 3:
            folderPath = TEXT_TEST_PATH
        else:
            print("This option doesn't exist, please choose again!")
            continue

        try:
            fileList = os.listdir(folderPath)
        except FileNotFoundError:
            print("Folder not found for this option.")
            continue

        if not fileList:
            print("No files added to this folder yet.")
            continue

        print("Files available for decompress:")
        for i, fname in enumerate(fileList, start=1):
            print(f"({i}) {fname}")
        print("(0) Return")

        try:
            userChoosed = int(input("Choose the file: "))
        except ValueError:
            print("Invalid input, must be a number.")
            continue

        if userChoosed == 0:
            continue
        elif 1 <= userChoosed <= len(fileList):
            fileChoosed = os.path.join(folderPath, fileList[userChoosed - 1])
            return fileChoosed
        else:
            print("Invalid option, try again.")

if __name__ == '__main__':
	while True:
		fileName = GZIPmenu()
		
		if fileName is None:
			break

		if len(sys.argv) > 1:
			fileName = sys.argv[1]

		gz = GZIP(fileName)
		gz.decompress()

		print("\n✅ File successfully unzipped!\n")
