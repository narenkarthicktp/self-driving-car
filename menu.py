import pygame

pygame.font.init()

DEFAULT_FONT = 'consolas'

class text():

	def __init__( self, size, xy, font = DEFAULT_FONT) -> None:

		self.font = pygame.font.Font( pygame.font.match_font(font), size[1])
		self.xy = xy

	def display( self, surface, data):

		buffer = self.font.render( data, True, (255,255,255))
		surface.blit( buffer, buffer.get_rect(center = self.xy))

class button():

	def __init__( self, size, xy, img, name = '') -> None:

		self.rect = pygame.Rect( xy, size)
		self.img = pygame.transform.scale( pygame.image.load(img), size)
		self.label = text( (size[0],14), (xy[0], xy[1]+32))
		self.name = name
		self.rect.center = xy

	def display( self, surface):

		surface.blit( self.img, self.rect)
		if self.name != '':
			self.label.display( surface, self.name)

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
		self.name = self.set_txt if toggle_condition else self.unset_txt
		return super().display(surface)

pygame.font.quit()
