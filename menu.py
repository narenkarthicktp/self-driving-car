import pygame

pygame.font.init()

# print(pygame.font.get_fonts())

class button():

	def __init__( self, size, xy, img, txt = 'None') -> None:

		self.rect = pygame.Rect( xy, size)
		self.img = pygame.transform.scale( pygame.image.load(img), size)
		self.surface = pygame.Surface( size, pygame.SRCALPHA)
		self.label = text( (size[0],14), (xy[0], xy[1]+32))
		self.txt = txt
		self.rect.center = xy

	def display( self, surface):

		# self.surface.fill( ( 0, 0, 0))
		surface.blit( self.img, self.rect)
		self.label.display( surface, self.txt)

	def listen( self, mousebutton):

		if mousebutton:
			if self.rect.collidepoint(pygame.mouse.get_pos()):
				return True
		return False

class toggle(button):

	def __init__(self, size, xy, img, alt_img, txt, alt_txt) -> None:

		self.set_img = pygame.transform.scale( pygame.image.load(img), size)
		self.unset_img = pygame.transform.scale( pygame.image.load(alt_img), size)
		self.set_txt = txt
		self.unset_txt = alt_txt
		self.set = True
		super().__init__( size, xy, img)

	def display(self, surface, toggle_condition):

		self.img = self.set_img if toggle_condition else self.unset_img
		self.txt = self.set_txt if toggle_condition else self.unset_txt
		return super().display(surface)

class text():

	def __init__( self, size, xy, font = 'consolas') -> None:

		self.font = pygame.font.Font( pygame.font.match_font(font), size[1])
		self.surface = pygame.Surface( size, pygame.SRCALPHA)
		self.xy = xy

	def display( self, surface, data):

		buffer = self.font.render( data, True, (255,255,255))
		surface.blit( buffer, buffer.get_rect(center = self.xy))

pygame.font.quit()