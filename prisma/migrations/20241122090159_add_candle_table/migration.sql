/*
  Warnings:

  - You are about to drop the column `candles` on the `analized_candles` table. All the data in the column will be lost.
  - You are about to drop the column `created_at` on the `analized_candles` table. All the data in the column will be lost.
  - You are about to drop the column `updated_at` on the `analized_candles` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[candle_uuid]` on the table `analized_candles` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `candle_uuid` to the `analized_candles` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "analized_candles" DROP COLUMN "candles",
DROP COLUMN "created_at",
DROP COLUMN "updated_at",
ADD COLUMN     "candle_uuid" TEXT NOT NULL;

-- CreateTable
CREATE TABLE "candles" (
    "uuid" TEXT NOT NULL,
    "date" TIMESTAMP(3) NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "volume" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "candles_pkey" PRIMARY KEY ("uuid")
);

-- CreateIndex
CREATE UNIQUE INDEX "analized_candles_candle_uuid_key" ON "analized_candles"("candle_uuid");

-- AddForeignKey
ALTER TABLE "analized_candles" ADD CONSTRAINT "analized_candles_candle_uuid_fkey" FOREIGN KEY ("candle_uuid") REFERENCES "candles"("uuid") ON DELETE CASCADE ON UPDATE CASCADE;
