-- CreateTable
CREATE TABLE "analized_candles" (
    "uuid" TEXT NOT NULL,
    "ai_analysis" TEXT NOT NULL,
    "candles" JSONB[],
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "analized_candles_pkey" PRIMARY KEY ("uuid")
);
