"""pygame slideshow display service."""

from pathlib import Path
from random import Random
from typing import Any

from hummel_it_frame.config import AppConfig, load_config
from hummel_it_frame.display.logic import calculate_image_placement, discover_images


class PygameSlideshow:
    """Run a fullscreen pygame slideshow from the configured image directory."""

    def __init__(
        self,
        config: AppConfig | None = None,
        *,
        random_generator: Random | None = None,
    ) -> None:
        self._config = config or load_config()
        self._random = random_generator or Random()
        self._image_queue: list[Path] = []
        self._known_images: set[Path] = set()

    def run(self) -> None:
        """Start the fullscreen slideshow."""
        import pygame

        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Hummel IT Frame")
        clock = pygame.time.Clock()

        try:
            self._run_loop(pygame, screen, clock)
        finally:
            pygame.quit()

    def _run_loop(self, pygame: Any, screen: Any, clock: Any) -> None:
        interval_ms = self._config.slideshow.interval_seconds * 1000
        next_slide_at = 0
        current_surface = None
        running = True

        while running:
            running = self._handle_events(pygame)
            now = pygame.time.get_ticks()

            if now >= next_slide_at:
                current_surface = self._load_next_surface(pygame)
                next_slide_at = now + interval_ms

            if current_surface is None:
                self._draw_placeholder(pygame, screen)
            else:
                self._draw_image(pygame, screen, current_surface)

            pygame.display.flip()
            clock.tick(30)

    @staticmethod
    def _handle_events(pygame: Any) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key in {
                pygame.K_ESCAPE,
                pygame.K_q,
            }:
                return False

        return True

    def _load_next_surface(self, pygame: Any) -> Any | None:
        self._refresh_image_queue()

        while self._image_queue:
            image_path = self._image_queue.pop(0)
            try:
                return pygame.image.load(str(image_path)).convert()
            except (OSError, pygame.error):
                continue

        return None

    def _refresh_image_queue(self) -> None:
        images = discover_images(self._config.storage.image_directory)
        image_set = set(images)
        if image_set != self._known_images or not self._image_queue:
            self._known_images = image_set
            self._image_queue = images
            self._random.shuffle(self._image_queue)

    def _draw_image(self, pygame: Any, screen: Any, image: Any) -> None:
        screen.fill((0, 0, 0))
        placement = calculate_image_placement(
            image.get_size(),
            screen.get_size(),
            self._config.display.mode,
        )
        scaled_image = pygame.transform.smoothscale(
            image,
            (placement.width, placement.height),
        )
        screen.blit(scaled_image, (placement.x, placement.y))

    @staticmethod
    def _draw_placeholder(pygame: Any, screen: Any) -> None:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 48)
        text_surface = font.render("No images available", True, (255, 255, 255))
        screen_rect = screen.get_rect()
        text_rect = text_surface.get_rect(center=screen_rect.center)
        screen.blit(text_surface, text_rect)


def run_slideshow(config: AppConfig | None = None) -> None:
    """Run the pygame slideshow service."""
    PygameSlideshow(config).run()


def main() -> None:
    """Console entrypoint for the display service."""
    run_slideshow()


if __name__ == "__main__":
    main()
