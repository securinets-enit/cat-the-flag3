
const puppeteer = require('puppeteer');

function createBot({ internalBase, adminToken, visitMs = 3500, log = console.log }) {
  let browser = null;
  const queue = [];
  let running = false;

  async function getBrowser() {
    if (browser && browser.connected) return browser;
    browser = await puppeteer.launch({
      headless: 'new',
      executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || undefined,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
      ],
    });
    return browser;
  }

  async function visit(targetUrl) {
    const b = await getBrowser();
    const page = await b.newPage();
    try {
      const u = new URL(internalBase);
      await page.setCookie({
        name: 'session',
        value: adminToken,
        domain: u.hostname,
        path: '/',
        httpOnly: true,
        sameSite: 'Lax',
      });

      log(`[bot] admin visiting ${targetUrl}`);
      await page.goto(targetUrl, { waitUntil: 'networkidle2', timeout: 8000 });
      await new Promise((r) => setTimeout(r, visitMs));
      log(`[bot] done ${targetUrl}`);
    } catch (err) {
      log(`[bot] error on ${targetUrl}: ${err.message}`);
    } finally {
      await page.close().catch(() => {});
    }
  }

  async function drain() {
    if (running) return;
    running = true;
    try {
      while (queue.length) {
        const job = queue.shift();
        await visit(job);
      }
    } finally {
      running = false;
    }
  }

  return {
    enqueue(targetUrl) {
      queue.push(targetUrl);
      drain();
    },
    queueLength: () => queue.length,
    async close() {
      if (browser) await browser.close().catch(() => {});
    },
  };
}

module.exports = { createBot };
